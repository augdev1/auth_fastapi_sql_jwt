# Auth FastAPI - Segurança em Foco

API de autenticação moderna e segura construída com FastAPI, focada em Identity and Access Management (IAM) e mitigação de vulnerabilidades comuns de autenticação.

Este projeto foi desenvolvido para aplicar conceitos reais de Cibersegurança (Blue Team/AppSec) no desenvolvimento backend, implementando defesa em profundidade com tokens JWT, autenticação multifator (MFA/2FA) e auditoria de logs.

(Insira aqui um print ou GIF curto da interface do Swagger ou da geração do QR Code)

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

## Configuração do .env

Antes de executar a aplicação, crie um arquivo `.env` na raiz do projeto e adicione as variáveis de configuração do banco de dados:

```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=seu_banco
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
```

Certifique-se de que essas variáveis correspondem às configurações do seu banco de dados PostgreSQL.

## Executando a Aplicação

Para executar a aplicação, use o uvicorn:

```bash
uvicorn main:app --reload
```

A aplicação estará disponível em `http://127.0.0.1:8000`.

Você pode acessar a documentação interativa da API em `http://127.0.0.1:8000/docs`.