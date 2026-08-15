# Auth FastAPI - Segurança em Foco & Interface Glassmorphism

API de autenticação moderna e segura construída com FastAPI, focada em Identity and Access Management (IAM), autenticação JWT e multifator (2FA/TOTP), acompanhada de uma **Interface Web SPA (Single Page Application) em Glassmorphism Preto & Dourado**.

![AuthFastAPI Black & Gold UI](https://img.shields.io/badge/UI-Black%20%26%20Gold%20Glassmorphism-d4af37?style=for-the-badge)
![FastAPI](https://img.shields.io/badge/FastAPI-0.134+-009688?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python)

---

## 🎨 Interface Web (Black & Gold Glassmorphism)

O projeto possui uma **Single Page Application (SPA)** responsiva embutida, servida diretamente na rota `/` (`http://localhost:8000/`):

- **Design System Premium**: Visual em tom obsidiana e dourado champanhe com transparências `backdrop-filter: blur(16px)` e brilhos neon dourados.
- **Fluxo de Login & Registro**: Alternância suave por abas e suporte a validação de token JWT.
- **Modal Interativo 2FA**: Ao tentar logar com 2FA ativado, o sistema abre automaticamente um modal para inserção do código de 6 dígitos.
- **Gerenciador TOTP**: Gerador de QR Code em tempo real (Base64) para escaneamento no Google Authenticator / Authy, cópia rápida da chave secreta e validação.
- **Trilha de Auditoria (Logs)**: Interface visual para registrar novas ações e listar o histórico completo de logs de segurança.
- **Testador de Rotas**: Botão de teste para disparar chamadas autenticadas para `GET /protected`.
- **100% Responsivo**: Layout otimizado para navegação em Smartphones, Tablets e Desktops.

---

## 🔐 Destaques de Segurança (Security Features)

- **Defesa contra Brute Force/Credential Stuffing:**
  - Implementação de Autenticação em Duas Etapas (2FA) via algoritmo TOTP (Time-based One-Time Password), integrado com aplicativos como Google Authenticator e Authy.

- **Gerenciamento Seguro de Sessão:**
  - Uso de JSON Web Tokens (JWT) com suporte a tokens temporários de curta duração durante a etapa intermediária do 2FA.

- **Proteção de Dados em Repouso:**
  - Senhas de usuários salvas utilizando hashing forte (PBKDF2 / Bcrypt com salting).

- **Trilha de Auditoria (Logging):**
  - Registro de ações de login, geração de 2FA e ações personalizadas dos usuários em banco de dados e arquivo de log.

- **Fallback de Banco de Dados Flexível:**
  - Suporte automático a **PostgreSQL** ou fallback para **SQLite local (`sqlite:///./app.db`)** caso o serviço Postgres não esteja configurado, permitindo rodar a aplicação instantaneamente.

---

## ⚙️ Estrutura do Projeto

```
.
├── app/                  # Pacote da Aplicação FastAPI
│   ├── __init__.py
│   ├── main.py           # Aplicação FastAPI e rotas
│   ├── auth.py           # Regras de Autenticação (JWT, TOTP/2FA)
│   ├── crud.py           # Operações de Banco de Dados
│   ├── database.py       # Conexão SQLAlchemy e fallback SQLite
│   ├── models.py         # Modelos de Tabelas ORM
│   ├── schemas.py        # Schemas Pydantic
│   └── static/           # Interface Web SPA Glassmorphism
│       ├── index.html    # Estrutura HTML5 da SPA
│       ├── style.css     # Design System Preto & Dourado Glassmorphism
│       └── app.js        # Lógica Frontend, Fetch API, JWT & 2FA
├── migrations/           # Migrações do banco via Alembic
├── alembic.ini           # Configuração do Alembic
├── poetry.lock
├── pyproject.toml
├── README.md
└── requirements.txt
```

---

## 🔌 Endpoints da API

- `GET /` - Serve a Interface Web SPA (Glassmorphism).
- `GET /health` - Verificação de status da API.
- `POST /register` - Registro de novo usuário.
- `POST /login` - Login inicial. Retorna `access_token` ou `temp_token` (se o 2FA estiver ativo).
- `POST /login/2fa` - Validação do código TOTP com `temp_token` para obter o `access_token` final.
- `GET /protected` - Endpoint de exemplo protegido exigindo Bearer Token.
- `POST /2fa/setup` - Gera novo segredo TOTP e QR Code em Base64 para o usuário logado.
- `POST /2fa/verify` - Valida o código de 6 dígitos para confirmação da ativação do 2FA.
- `POST /generate-qrcode` - Gera imagem PNG de QR Code a partir de uma URL OTPAuth.
- `POST /logs` - Adiciona uma nova entrada de log para o usuário autenticado.
- `GET /logs` - Retorna a lista de logs do usuário autenticado.

Documentação Swagger/OpenAPI interativa: `http://127.0.0.1:8000/docs`

---

## 🚀 Como Executar

### 1. Clonar o Repositório

```bash
git clone https://github.com/augdev1/auth_fastapi_sql_jwt.git
cd auth_fastapi_sql_jwt
```

### 2. Instalar Dependências

Usando `pip`:
```bash
pip install -r requirements.txt
```

Ou usando `poetry`:
```bash
poetry install
```

### 3. Iniciar o Servidor

Execute o Uvicorn com o módulo da aplicação:

```bash
python -m uvicorn app.main:app --reload
```

Acesse a interface gráfica no seu navegador:
👉 **[http://127.0.0.1:8000](http://127.0.0.1:8000)**

