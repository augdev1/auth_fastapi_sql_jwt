# Auth FastAPI com PostgreSQL

Este é um sistema de autenticação robusto desenvolvido com **FastAPI** e **PostgreSQL**. O projeto inclui registro de usuários, login com geração de tokens JWT (JSON Web Tokens), rotas protegidas e um sistema de log de atividades salvo no banco de dados.

## 🚀 Tecnologias Utilizadas

- **Python 3.8+**
- **FastAPI**: Framework web moderno e rápido.
- **SQLAlchemy**: ORM para interação com o banco de dados.
- **PostgreSQL**: Banco de dados relacional.
- **Python-Jose**: Para criação e verificação de tokens JWT.
- **Passlib**: Para hash de senhas (configurado com `pbkdf2_sha256`).

## ⚙️ Pré-requisitos

Antes de começar, certifique-se de ter instalado:
- Python
- PostgreSQL

## 🗄️ Configuração do Banco de Dados

O projeto está configurado para conectar-se a um banco de dados PostgreSQL local.

1. Crie um banco de dados chamado `cyberdb` no seu PostgreSQL.
2. Verifique as credenciais no arquivo `database.py`. A configuração atual espera:
   - **Usuário:** `postgres`
   - **Senha:** `qwerty123`
   - **Host:** `localhost`
   - **Porta:** `5432`
   - **Banco:** `cyberdb`

> **Nota:** Se suas credenciais forem diferentes, altere a variável `SQLALCHEMY_DATABASE_URL` no arquivo `database.py`.

## 📦 Instalação

1. Clone o repositório ou baixe os arquivos.
2. Crie um ambiente virtual (recomendado):
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # Linux/Mac
   source .venv/bin/activate
   ```
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

## ▶️ Executando a Aplicação

Para iniciar o servidor de desenvolvimento, execute:

```bash
uvicorn main:app --reload
```

O servidor iniciará em `http://127.0.0.1:8000`.

## 📚 Documentação da API (Swagger UI)

O FastAPI gera automaticamente a documentação interativa. Após iniciar o servidor, acesse:

- **Swagger UI:** http://127.0.0.1:8000/docs
- **ReDoc:** http://127.0.0.1:8000/redoc

## 🔗 Endpoints Principais

### Autenticação
- `POST /register`: Cria um novo usuário.
  - Body: `{"username": "seu_usuario", "password": "sua_senha"}`
- `POST /login`: Autentica o usuário e retorna um `access_token`.
  - Body: `{"username": "seu_usuario", "password": "sua_senha"}`

### Rotas Protegidas (Requer Token Bearer)
Para acessar estas rotas, você deve enviar o token no header: `Authorization: Bearer <token>`.

- `GET /protected`: Retorna uma mensagem de sucesso e o nome do usuário logado.
- `POST /logs`: Salva uma ação de log no banco de dados vinculada ao usuário atual.
  - Body: `{"user_id": 0, "action": "Descrição da ação"}` (O `user_id` no body é ignorado em favor do usuário autenticado, mas o schema atual o solicita).

### Utilitários
- `GET /health`: Checagem de saúde da API (`{"status": "ok"}`).

## 📂 Estrutura de Arquivos

- `main.py`: Ponto de entrada da aplicação e definição das rotas.
- `models.py`: Modelos do banco de dados (Tabelas `users` e `logs`).
- `schemas.py`: Modelos Pydantic para validação de dados (Request/Response).
- `crud.py`: Funções para criar, ler e atualizar dados no banco.
- `auth.py`: Lógica de segurança (Hash de senha e Tokens JWT).
- `database.py`: Configuração da conexão com o PostgreSQL.

## 📝 Logs do Sistema

Além dos logs salvos no banco de dados via endpoint, a aplicação gera um arquivo local chamado `app.log` contendo informações sobre logins e acessos.

---