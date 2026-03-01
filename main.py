from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
import logging
import crud, schemas, auth, database, models
from database import get_db

app = FastAPI()
models.Base.metadata.create_all(bind=database.engine) # Cria as tabelas no banco de dados com base nos modelos definidos em models.py

security = HTTPBearer()
logging.basicConfig(filename='app.log', level=logging.INFO)

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

@app.post("/login", response_model=schemas.Token)
def login(user: schemas.UserLogin, db: Session = Depends(database.get_db)):
    db_user = crud.get_user(db, username=user.username)
    if not db_user or not crud.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    access_token = auth.create_access_token(data={"sub": db_user.username})
    logging.info(f"Login: {user.username}")
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/protected")
def protected(current_user: models.User = Depends(get_current_user)):
    logging.info(f"Access: {current_user.username}")
    return {"msg": "This is a protected endpoint", "user": current_user.username}

@app.post("/logs")
def add_log(log: schemas.Log, current_user: models.User = Depends(get_current_user), db: Session = Depends(database.get_db)):
       crud.create_log(db, user_id=current_user.id, action=log.action)
       return {"message": "Log added successfully"}