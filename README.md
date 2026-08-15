# Auth FastAPI - Segurança em Foco & Interface Glassmorphism

API de autenticação moderna e segura construída com FastAPI, focada em Identity and Access Management (IAM), autenticação JWT e multifator (2FA/TOTP) **totalmente integrada ao Google Authenticator**, acompanhada de uma **Interface Web SPA (Single Page Application) em Glassmorphism Preto & Dourado**.

![2FA Google Authenticator](https://img.shields.io/badge/2FA-Google%20Authenticator-4285F4?style=for-the-badge&logo=google-authenticator&logoColor=white)
![AuthFastAPI Black & Gold UI](https://img.shields.io/badge/UI-Black%20%26%20Gold%20Glassmorphism-d4af37?style=for-the-badge)
![FastAPI](https://img.shields.io/badge/FastAPI-0.134+-009688?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python)

---

## 🔑 Destaque: Autenticação 2FA com Google Authenticator

> [!IMPORTANT]
> **Boas Práticas de AppSec & IAM (Defesa em Profundidade)**  
> Este projeto implementa o padrão industrial **RFC 6238 (TOTP - Time-based One-Time Password)** com compatibilidade direta e nativa com o **Google Authenticator**.
>
> **Como Funciona a Proteção 2FA:**
> 1. **Vinculação Instantânea**: O backend gera um segredo Base32 único e converte a URL `otpauth://` em um **QR Code dinâmico**.
> 2. **Pareamento**: O usuário escaneia o QR Code utilizando a câmera do aplicativo **Google Authenticator**.
> 3. **Login em 2 Etapas**: Ao realizar login com usuário e senha, o servidor emite um `temp_token` temporário de 3 minutos e exige a validação do código de 6 dígitos gerado em tempo real pelo **Google Authenticator** antes de liberar o `access_token` JWT definitivo.

---

## 📸 Projeto em Funcionamento

### Token de Acesso após logar no usuário criado
<img width="1920" height="1080" alt="token_api" src="https://github.com/user-attachments/assets/830211b5-b719-4cf3-82f6-332777c7d294" />

### Gerador de QR Code após vinculação com o Google Authenticator
<img width="1920" height="639" alt="qr_code_gerado" src="https://github.com/user-attachments/assets/3a57d0a3-8078-4e9a-91b6-25250a76b017" />

### Login com Autenticação de dois fatores usando o `temp_token` e o código gerado pelo Google Authenticator
<img width="1920" height="1080" alt="login_c_2fa" src="https://github.com/user-attachments/assets/23ff1f42-da26-4d7e-be66-9c7fca12a5aa" />

---

## 🎨 Interface Web (Black & Gold Glassmorphism)
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/555493bd-1f27-43ce-b70d-c47dcfbcc494" />


O projeto possui uma **Single Page Application (SPA)** responsiva embutida, servida diretamente na rota `/` (`http://localhost:8000/`):

- **Design System Premium**: Visual em tom obsidiana e dourado champanhe com transparências `backdrop-filter: blur(16px)` e brilhos neon dourados.
- **Fluxo de Login & Registro**: Alternância suave por abas e suporte a validação de token JWT.
- **Modal Interativo 2FA**: Ao tentar logar com 2FA ativado, o sistema abre automaticamente um modal para inserção do código de 6 dígitos gerado no Google Authenticator.
- **Gerenciador TOTP**: Gerador de QR Code em tempo real (Base64) para escaneamento direto no Google Authenticator, cópia rápida da chave secreta e validação.
- **Trilha de Auditoria (Logs)**: Interface visual para registrar novas ações e listar o histórico completo de logs de segurança.
- **Testador de Rotas**: Botão de teste para disparar chamadas autenticadas para `GET /protected`.
- **100% Responsivo**: Layout otimizado para navegação em Smartphones, Tablets e Desktops.

---

## 🔐 Recursos de Segurança (Security Features)

- **Defesa contra Brute Force & Credential Stuffing:**
  - Autenticação Multifator (MFA/2FA) via algoritmo TOTP com **Google Authenticator**.

- **Gerenciamento Seguro de Sessão:**
  - JSON Web Tokens (JWT) com tokens temporários de curta duração durante a verificação de 2FA.

- **Proteção de Dados em Repouso:**
  - Hashing forte de senhas com PBKDF2 / Bcrypt e salting.

- **Trilha de Auditoria (Logging):**
  - Registro detalhado de logins, alterações de 2FA e ações do usuário em banco de dados e arquivo de log.

- **Fallback de Banco de Dados Flexível:**
  - Suporte a **PostgreSQL** ou fallback para **SQLite local (`sqlite:///./app.db`)** sem necessidade de configurações complexas.

---

## ⚙️ Estrutura do Projeto

```
.
├── app/                  # Pacote da Aplicação FastAPI
│   ├── __init__.py
│   ├── main.py           # Aplicação FastAPI e rotas
│   ├── auth.py           # Regras de Autenticação (JWT, Google Authenticator / 2FA)
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
├── README.md             # Documentação do projeto
└── requirements.txt
```

---

## 🔌 Endpoints da API

- `GET /` - Serve a Interface Web SPA (Glassmorphism).
- `GET /health` - Verificação de status da API.
- `POST /register` - Registro de novo usuário.
- `POST /login` - Login inicial. Retorna `access_token` ou `temp_token` (se o 2FA com Google Authenticator estiver ativo).
- `POST /login/2fa` - Validação do código TOTP do Google Authenticator com `temp_token` para obter o `access_token` final.
- `GET /protected` - Endpoint de exemplo protegido exigindo Bearer Token.
- `POST /2fa/setup` - Gera novo segredo TOTP e QR Code em Base64 para pareamento com o Google Authenticator.
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
