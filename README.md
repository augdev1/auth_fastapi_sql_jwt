# Auth FastAPI https://icons8.com.br/icon/ZeaY7GVy1j1L/api |  SQL 🛢️ |  JWT 🔐 | TOTP 🔑 | GOOGLE AUTHENTICATOR 🇬 Google | QR CODE ⛶ 
API de autenticação moderna construída com FastAPI, JWT, TOTP (2FA) e SQLAlchemy, focada em boas práticas de segurança e organização de código para aplicações reais em produção.

Este projeto foi desenvolvido para demonstrar domínio de backend em Python, desde modelagem de usuários e tokens até autenticação em duas etapas integrada com apps como Google Authenticator.

## Funcionalidades

- Registro de usuário
- Login de usuário com token JWT
- Autenticação de dois fatores (2FA) usando TOTP
- Geração de QR Code para configuração fácil do 2FA em aplicativos de autenticação
- Endpoints protegidos
- Registro de ações do usuário
- Migrações de banco de dados com Alembic

## Estrutura do Projeto

```
.
├── alembic.ini
├── app.log
├── auth.py
├── crud.py
├── database.py
├── main.py
├── models.py
├── poetry.lock
├── pyproject.toml
├── README.md
├── requirements.txt
├── schemas.py
├── .git/
├── .venv/
├── .vscode/
│   └── settings.json
└── migrations/
    ├── env.py
    ├── README
    ├── script.py.mako
    └── versions/
```

## Começando

### Pré-requisitos

- Python 3.10+
- Poetry
- PostgreSQL

### Instalação

1.  **Clone o repositório:**

    ```bash
    git clone <url-do-repositorio>
    cd auth-fastapi
    ```

2.  **Instale as dependências usando o Poetry:**

    ```bash
    poetry install
    ```

3.  **Configure o banco de dados:**

    Certifique-se de ter um banco de dados PostgreSQL criado. Atualize a URL do banco de dados em `database.py`:

    ```python
    SQLALCHEMY_DATABASE_URL = "postgresql://usuario:senha@host:porta/nomedobanco"
    ```

4.  **Execute as migrações do banco de dados:**

    Atualize a `sqlalchemy.url` em `alembic.ini` para corresponder à sua string de conexão do banco de dados e execute:

    ```bash
    alembic upgrade head
    ```

### Executando a Aplicação

Para executar a aplicação, use o uvicorn:

```bash
uvicorn main:app --reload
```

A aplicação estará disponível em `http://127.0.0.1:8000`.

## Endpoints da API

- `GET /health`: Verificação de saúde.
- `POST /register`: Registro de usuário.
- `POST /login`: Login de usuário. Retorna um token temporário se o 2FA estiver ativado.
- `POST /login/2fa`: Verifica o código 2FA e obtém um token de acesso final.
- `GET /protected`: Um endpoint protegido que requer autenticação.
- `POST /logs`: Adiciona uma entrada de log para o usuário atual.
- `POST /2fa/setup`: Configura o 2FA para o usuário atual, retornando um QR Code para ser lido por aplicativos de autenticação.
- `POST /2fa/verify`: Verifica o código 2FA.

Você pode acessar a documentação interativa da API em `http://127.0.0.1:8000/docs`.
