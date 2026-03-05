# 🛡️ Secure Auth API | FastAPI | PostgreSQL | JWT | 2FA (TOTP)

API de autenticação moderna e segura construída com FastAPI, focada em **Identity and Access Management (IAM)** e mitigação de vulnerabilidades comuns de autenticação. 

Este projeto foi desenvolvido para aplicar conceitos reais de Cibersegurança (Blue Team/AppSec) no desenvolvimento backend, implementando defesa em profundidade com tokens JWT, autenticação multifator (MFA/2FA) e auditoria de logs.

*(Insira aqui um print ou GIF curto da interface do Swagger ou da geração do QR Code)*

## 🔐 Destaques de Segurança (Security Features)

- **Defesa contra Brute Force/Credential Stuffing:** Implementação de Autenticação em Duas Etapas (2FA) via algoritmo TOTP (Time-based One-Time Password), integrado com Google Authenticator.
- **Gerenciamento Seguro de Sessão:** Uso de JSON Web Tokens (JWT) com tempo de expiração curto para tokens de acesso.
- **Proteção de Dados em Repouso:** Senhas de usuários NUNCA são salvas em texto claro (utilizando hashing forte - Bcrypt).
- **Trilha de Auditoria (Logging):** Registro de ações de login e acesso a endpoints críticos, fundamental para análise em SOC e resposta a incidentes.
- **Prevenção de Vazamento de Credenciais:** Configuração baseada estritamente em Variáveis de Ambiente (`.env`).

## ⚙️ Funcionalidades
- Registro de usuário e Login seguro.
- Geração de QR Code dinâmico para pareamento de aplicativos autenticadores.
- Endpoints protegidos exigindo validação de token Bearer.
- Migrações de banco de dados rastreáveis com Alembic.

## 🚀 Começando

### Pré-requisitos
- Python 3.10+
- Poetry
- PostgreSQL

### Instalação Segura

1. **Clone o repositório:**
   ```bash
   git clone <url-do-repositorio>
   cd auth-fastapi

Instale as dependências usando o Poetry:

 ```bash
poetry install
```
Configuração de Variáveis de Ambiente (Segurança):
Crie um arquivo chamado .env na raiz do projeto baseado no arquivo de exemplo. Nunca adicione o arquivo .env ao seu commit!
code
 ```bash
cp .env.example .env
```
Edite o arquivo .env com suas credenciais do banco de dados e chave secreta do JWT.
Execute as migrações do banco de dados:
```bash
alembic upgrade head
```
Executando a Aplicação
```bash
uvicorn main:app --reload
```
Acesse a documentação interativa (Swagger UI) em: http://127.0.0.1:8000/docs.
📍 Endpoints Críticos da API
```
POST /register: Criação de identidade.
POST /login: Autenticação primária (retorna token provisório se 2FA ativo).
POST /login/2fa: Validação do desafio TOTP e emissão do token final.
POST /2fa/setup: Gera seed e QR Code para aplicativos de MFA.
POST /logs: Geração de trilha de auditoria do usuário.
```
