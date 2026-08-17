# NutriTrack — AC1

Sistema web para registro de alimentação e acompanhamento de hábitos nutricionais.

## AC1 — Funcionalidades
- Cadastro de usuário
- Login
- Logout no front-end
- Cadastro de alimentos
- Listagem de alimentos
- API REST
- Banco de dados
- Front-end consumindo a API

## Stack
- Front-end: React + Vite
- Back-end: Python + FastAPI
- Banco: SQLite por padrão (fácil para apresentação) e preparado para PostgreSQL
- ORM: SQLAlchemy
- Autenticação: JWT

## Como executar

### Backend
```bash
cd backend
python -m venv .venv
# macOS/Linux:
source .venv/bin/activate
# Windows:
# .venv\Scripts\activate

pip install -r requirements.txt
uvicorn app.main:app --reload
```

API: http://127.0.0.1:8000
Documentação Swagger: http://127.0.0.1:8000/docs

### Frontend
Em outro terminal:
```bash
cd frontend
npm install
npm run dev
```

Abra o endereço mostrado pelo Vite, normalmente http://localhost:5173.

## Banco
Por padrão, o projeto usa SQLite e cria `backend/nutritrack.db` automaticamente.

Para PostgreSQL, defina:
`DATABASE_URL=postgresql+psycopg2://usuario:senha@localhost:5432/nutritrack`

## Fluxo da demonstração da AC1
1. Criar uma conta.
2. Fazer login.
3. Cadastrar um alimento.
4. Mostrar o alimento aparecendo na lista.
5. Abrir `/docs` e demonstrar os endpoints da API.
6. Mostrar o arquivo do banco sendo criado.
