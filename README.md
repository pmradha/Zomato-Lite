# Zomato-Lite

A V1 anonymous restaurant review app for Ludhiana Burrito in Sector 32.

## Architecture

`User -> Frontend -> API -> Backend -> Neon PostgreSQL`

- Frontend: React, Vite, TypeScript
- Backend/API: FastAPI, Python
- Database access: SQLAlchemy
- Database: Neon PostgreSQL

The existing Neon `restaurant` and `review` tables are authoritative. The SQLAlchemy models and [migration](backend/migrations/001_initial.sql) mirror that schema; the application does not create or replace tables at startup.

## Run the backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export DATABASE_URL='your Neon connection string'
uvicorn app.main:app --reload
```

Do not commit a real connection string. The API uses `DATABASE_URL` only on the backend.

## Run the frontend

```bash
cd frontend
npm install
npm run dev
```

The frontend expects the API at `http://localhost:8000`. Set `VITE_API_URL` to override it.
