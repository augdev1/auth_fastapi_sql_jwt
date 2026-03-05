from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse, StreamingResponse
from datetime import timedelta
from sqlalchemy.orm import Session
import logging
import crud, schemas, auth, database, models
from database import get_db

import qrcode
import io # Biblioteca para manipulação de arquivos em memória, usada para gerar a imagem do QR Code sem precisar salvar no disco
import base64 # Biblioteca para codificação e decodificação de dados em Base64, usada para converter a imagem do QR Code em uma string que pode ser facilmente transmitida na resposta da API
from io import BytesIO
import pyotp
from pydantic import BaseModel

class OTPAuthURLRequest(BaseModel):
    otpauth_url: str

class TOTPSetupResponse(BaseModel):
    secret: str
    qr_code_base64: str
    otpauth_url: str

app = FastAPI()
models.Base.metadata.create_all(bind=database.engine) # Cria as tabelas no banco de dados com base nos modelos definidos em models.py

security = HTTPBearer()
logging.basicConfig(filename='app.log', level=logging.INFO) # Configura o logging para registrar as atividades em um arquivo chamado app.log

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(database.get_db)): # Função para obter o usuário atual com base no token de autenticação
    payload = auth.verify_token(credentials.credentials)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = crud.get_user(db, username=payload.get("sub"))
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
    

#health check
@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/register")
def register(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = crud.get_user(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    crud.create_user(db=db, user=user)
    return {"msg": "user created"}

@app.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(database.get_db)):
    db_user = crud.get_user(db, username=user.username)
    if not db_user or not crud.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    # Se o 2FA estiver ativado, emita um token temporário que precisa ser verificado.
    if db_user.totp_secret:
        # Este token é de curta duração e tem um 'purpose' específico.
        temp_token = auth.create_access_token(
            data={"sub": db_user.username, "purpose": "2fa_login"},
            expires_delta=timedelta(minutes=3)
        )
        return JSONResponse(
            status_code=200,
            content={
                "message": "Two-factor authentication required",
                "temp_token": temp_token
            }
        )

    # Se o 2FA não estiver ativado, emita o token de acesso final diretamente.
    access_token = auth.create_access_token(data={"sub": db_user.username})
    logging.info(f"Login: {user.username}")
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/login/2fa", response_model=schemas.Token)
def login_2fa(data: schemas.TwoFactorLogin, db: Session = Depends(database.get_db)):
    payload = auth.verify_token(data.temp_token)
    if not payload or payload.get("purpose") != "2fa_login":
        raise HTTPException(status_code=401, detail="Invalid or expired temporary token")

    username = payload.get("sub")
    db_user = crud.get_user(db, username=username)
    if not db_user:
        raise HTTPException(status_code=401, detail="User from token not found")

    if not db_user.totp_secret or not auth.verify_totp(db_user.totp_secret, data.code):
        raise HTTPException(status_code=400, detail="Invalid TOTP code")

    # Se o código TOTP for válido, emita o token de acesso final.
    access_token = auth.create_access_token(data={"sub": db_user.username})
    logging.info(f"2FA Login successful: {db_user.username}")
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/protected")
def protected(current_user: models.User = Depends(get_current_user)):
    logging.info(f"Access: {current_user.username}")
    return {"msg": "This is a protected endpoint", "user": current_user.username}

@app.post("/logs")
def add_log(log: schemas.LogCreate, current_user: models.User = Depends(get_current_user), db: Session = Depends(database.get_db)):
       crud.create_log(db, user_id=current_user.id, action=log.action)
       return {"message": "Log added successfully"}

@app.post("/2fa/verify") #  Endpoint para verificar o código TOTP fornecido pelo usuário, garantindo que ele corresponda ao segredo armazenado no banco de dados para o usuário atual, e retornando uma mensagem de sucesso ou erro com base na verificação
def verify_2fa(verification: schemas.TOTPVerify, current_user: models.User = Depends(get_current_user)):
    if not current_user.totp_secret:
        raise HTTPException(status_code=400, detail="2FA not setup for this user")
    
    if not auth.verify_totp(current_user.totp_secret, verification.code):
        raise HTTPException(status_code=400, detail="Invalid TOTP code")
        
    return {"message": "TOTP verified successfully"}

# Endpoint para gerar QR Code
@app.post("/generate-qrcode")
def generate_qrcode(request: OTPAuthURLRequest):
    # Generate QR Code image
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(request.otpauth_url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    # Convert image to BytesIO for streaming
    img_byte_arr = BytesIO()
    img.save(img_byte_arr, format="PNG")
    img_byte_arr.seek(0)

    # Return the image as a StreamingResponse
    return StreamingResponse(img_byte_arr, media_type="image/png")

@app.post("/2fa/setup", response_model=schemas.TOTPSetupResponse)
def setup_2fa(current_user: models.User = Depends(get_current_user), db: Session = Depends(database.get_db)):
    # 1. Generate TOTP secret
    secret = pyotp.random_base32()

    # 2. Save the secret to the database
    crud.update_user_totp_secret(db, current_user.id, secret)

    # 3. Generate the TOTP URI
    issuer_name = "MyApp"  # Replace with your app's name
    otpauth_url = f"otpauth://totp/{issuer_name}:{current_user.username}?secret={secret}&issuer={issuer_name}"

    # 4. Generate QR Code as Base64
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(otpauth_url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

    # Return JSON response
    return schemas.TOTPSetupResponse(
        secret=secret,
        qr_code_base64=img_str,
        otpauth_url=otpauth_url
    )