# NutriTrack — AC2

Sistema web para registro de alimentação de acordo com a hora e acompanhamento de hábitos nutricionais.

## AC2 — Nova entrega
Registro, consulta por data, edição e exclusão de refeições com múltiplos alimentos e quantidades em gramas. Os registros são separados por usuário.

O guia `docs/AC2.md` contém o roteiro de apresentação, endpoints, critérios de validação e texto para o Board.

### Abrir no Mac
Dê dois cliques em `ABRIR_NUTRITRACK.command` e abra http://127.0.0.1:5173. Mantenha a janela do Terminal aberta durante o uso. Se houver outro NutriTrack rodando, encerre-o antes. O iniciador reutiliza o ambiente Python da AC1 quando disponível; em outro computador, instala as dependências em um ambiente próprio. Requer Python e Node.js/npm.

Ao iniciar a AC2 sobre um banco da AC1, as tabelas de refeições são criadas automaticamente, preservando usuários e alimentos. Uma instalação nova começa com banco vazio: crie sua conta e cadastre os alimentos pela interface.

## AC1 — Funcionalidades preservadas
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

## Apresentação e validação da AC2
Veja [o roteiro da AC2](docs/AC2.md) para demonstrar cadastro, edição, consulta e exclusão de refeições.

No diretório `backend`, execute:
```sh
python -m unittest discover -s tests -v
```
Os testes usam um banco temporário e verificam autenticação, persistência, validações e isolamento entre contas.

No diretório `frontend`, execute `npm run build` para validar a compilação.
