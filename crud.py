from sqlalchemy.orm import Session
from passlib.context import CryptContext
import models, schemas

pwd_context = CryptContext(
    schemes=["pbkdf2_sha256"],
    deprecated="auto",
)
# Função para gerar um hash da senha usando o algoritmo PBKDF2-SHA256, limitando a senha a 72 caracteres para evitar problemas de truncamento
def get_password_hash(password: str):
    return pwd_context.hash(password[:72])
# Função para verificar se a senha fornecida corresponde à senha hashada armazenada no banco de dados
def verify_password(plain_password: str, hashed_password: str):
    plain_password = plain_password[:72]
    return pwd_context.verify(plain_password, hashed_password)
# Função para obter um usuário do banco de dados com base no nome de usuário
def get_user(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()
# Função para criar um novo usuário no banco de dados, hashando a senha antes de armazená-la
def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
# Função para criar um novo log de ação no banco de dados, associando-o ao ID do usuário e à ação realizada
def create_log(db: Session, user_id: int, action: str):
    db_log = models.Log(user_id=user_id, action=action)
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

def get_logs(db: Session, user_id: int):
    return db.query(models.Log).filter(models.Log.user_id == user_id).all()

def update_user_totp_secret(db: Session, user_id: int, secret: str): # Função para atualizar o segredo TOTP de um usuário no banco de dados, associando o novo segredo ao ID do usuário
    user = db.query(models.User).filter(models.User.id == user_id).first()
    user.totp_secret = secret
    db.commit()
    db.refresh(user)
