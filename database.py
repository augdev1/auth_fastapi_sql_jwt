from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Formato: postgresql://usuario:senha@host:porta/nome_do_banco
# Exemplo: postgresql://postgres:123456@localhost:5432/meu_banco
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:qwerty123@localhost:5432/cyberdb"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()