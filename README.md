# Auth FastAPI - Segurança em Foco

API de autenticação moderna e segura construída com FastAPI, focada em Identity and Access Management (IAM) e mitigação de vulnerabilidades comuns de autenticação.

Este projeto foi desenvolvido para aplicar conceitos reais de Cibersegurança (Blue Team/AppSec) no desenvolvimento backend, implementando defesa em profundidade com tokens JWT, autenticação multifator (MFA/2FA) e auditoria de logs.

## 🔐 Destaques de Segurança (Security Features)

- **Defesa contra Brute Force/Credential Stuffing:**
  - Implementação de Autenticação em Duas Etapas (2FA) via algoritmo TOTP (Time-based One-Time Password), integrado com Google Authenticator.

- **Gerenciamento Seguro de Sessão:**
  - Uso de JSON Web Tokens (JWT) com tempo de expiração curto para tokens de acesso.

- **Proteção de Dados em Repouso:**
  - Senhas de usuários NUNCA são salvas em texto claro (utilizando hashing forte - Bcrypt).

- **Trilha de Auditoria (Logging):**
  - Registro de ações de login e acesso a endpoints críticos, fundamental para análise em SOC e resposta a incidentes.

- **Prevenção de Vazamento de Credenciais:**
  - Configuração baseada estritamente em Variáveis de Ambiente (.env).

## ⚙️ Funcionalidades

- Registro de usuário e Login seguro.
- Geração de QR Code dinâmico para pareamento de aplicativos autenticadores.
- Endpoints protegidos exigindo validação de token Bearer.
- Migrações de banco de dados rastreáveis com Alembic.

## Projeto em funcionamento:
TOKEN DE ACESSO APÓS LOGAR NO USER CRIADO
<img width="1920" height="1080" alt="token_api" src="https://github.com/user-attachments/assets/830211b5-b719-4cf3-82f6-332777c7d294" />

GERADOR DE QR CODE APÓS CRIAÇÃO DE USER
<img width="1920" height="639" alt="qr_code_gerado" src="https://github.com/user-attachments/assets/3a57d0a3-8078-4e9a-91b6-25250a76b017" />

LOGIN COM AUTENTICAÇÃO DE DOIS FATORES USANDO O "temp_token" recebido do endpoint "Login" E DO "code" QUE É GERADO APÓS VINCULAÇÃO COM O GOOGLE AUTHENTICATOR
<img width="1920" height="1080" alt="login_c_2fa" src="https://github.com/user-attachments/assets/23ff1f42-da26-4d7e-be66-9c7fca12a5aa" />

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

## Endpoints da API

- `GET /health`: Verificação de saúde.
- `POST /register`: Registro de usuário.
- `POST /login`: Login de usuário. Retorna um token temporário se o 2FA estiver ativado.
- `POST /login/2fa`: Verifica o código 2FA e obtém um token de acesso final.
- `GET /protected`: Um endpoint protegido que requer autenticação.
- `POST /logs`: Adiciona uma entrada de log para o usuário atual.
- `POST /2fa/verify`: Verifica o código 2FA.
- `POST /generate-qrcode`: Recebe o otpauth_url no corpo da requisição e retorna a imagem PNG do QR Code.
- `POST /2fa/setup`: Configura o 2FA para o usuário atual, retornando um QR Code para ser lido por aplicativos de autenticação.

Você pode acessar a documentação interativa da API em `http://127.0.0.1:8000/docs`.

## Instalação

### Pré-requisitos

- Python 3.10+
- Poetry
- PostgreSQL

### Passos

1. **Clone o repositório:**

    ```bash
    git clone https://github.com/augdev1/auth_fastapi_sql_jwt.git
    cd auth-fastapi
    ```

2. **Instale as dependências usando o Poetry:**

    ```bash
    poetry install
    ```

3. **Configure o banco de dados:**

    Antes de executar a aplicação, crie um arquivo `.env` na raiz do projeto e adicione as variáveis de configuração do banco de dados:

    ```
    DB_HOST=localhost
    DB_PORT=5432
    DB_NAME=seu_banco
    DB_USER=seu_usuario
    DB_PASSWORD=sua_senha
    ```

    Certifique-se de que essas variáveis correspondem às configurações do seu banco de dados PostgreSQL.

4. **Execute as migrações do banco de dados:**

    Atualize a `sqlalchemy.url` em `alembic.ini` para corresponder à sua string de conexão do banco de dados e execute:

    ```bash
    alembic upgrade head
    ```

5. **Execute a aplicação:**

    Para executar a aplicação, use o uvicorn:

    ```bash
    uvicorn main:app --reload
    ```

    A aplicação estará disponível em `http://127.0.0.1:8000`.
