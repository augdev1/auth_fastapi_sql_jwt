from sqlalchemy import Column, Integer, String, func # Importa as classes necessárias do SQLAlchemy para definir os modelos de dados
from database import Base


class User(Base): # Define a classe User que representa a tabela de usuários no banco de dados
    __tablename__ = "users" # Especifica o nome da tabela no banco de dados
    id = Column(Integer, primary_key=True, index=True) # Define a coluna 'id' como chave primária e índice
    username = Column(String, unique=True, index=True) # Define a coluna 'username' como string, única e índice
    hashed_password = Column(String) # Define a coluna 'hashed_password' como string para armazenar a senha hashada
    totp_secret = Column(String, nullable=True) # Segredo para 2FA



class Log(Base): # Define a classe Log que representa a tabela de registros de log no banco de dados
    __tablename__ = "logs" # Especifica o nome da tabela no banco de dados
    id = Column(Integer, primary_key=True, index=True) # Define a coluna 'id' como chave primária e índice
    user_id = Column(Integer) # Define a coluna 'user_id' como inteiro para armazenar o ID do usuário associado ao log
    action = Column(String) # Define a coluna 'action' como string para armazenar a ação registrada no log
    timestamp = Column(String, server_default=func.now()) # Define a coluna 'timestamp' como string e atribui um valor padrão usando a função func.now() para registrar o horário do log