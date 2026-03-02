from datetime import datetime, timedelta
from jose import JWTError, jwt
import pyotp # Biblioteca para gerar e verificar códigos TOTP (Time-based One-Time Password) para autenticação de dois fatores (2FA)
SECRET_KEY = "seu-secret-super-seguro" # Em produção, use uma variável de ambiente para armazenar a chave secreta
ALGORITHM = "HS256" # Algoritmo de hashing para o token

def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=30)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None

def generate_totp_secret(): # Gera um segredo aleatório para o TOTP usando a biblioteca pyotp
    return pyotp.random_base32()

def get_totp_uri(username: str, secret: str): # Gera uma URI de provisionamento para o TOTP, que pode ser usada para criar um QR Code para configuração em aplicativos de autenticação
    return pyotp.totp.TOTP(secret).provisioning_uri(name=username, issuer_name="AuthFastAPI")

def verify_totp(secret: str, code: str): # Verifica se o código TOTP fornecido é válido para o segredo armazenado, usando a biblioteca pyotp
    return pyotp.TOTP(secret).verify(code)
