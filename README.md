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
export FRONTEND_ORIGIN='http://localhost:5173'
uvicorn app.main:app --reload
```

Do not commit a real connection string. The API uses `DATABASE_URL` only on the backend.

## Run the frontend

```bash
cd frontend
npm install
npm run dev
```

The frontend uses the Vite `/api` proxy locally. For a deployed frontend, set the public `VITE_API_URL` environment variable to the deployed backend URL. Configure the backend's `FRONTEND_ORIGIN` to the deployed frontend origin. Never expose `DATABASE_URL` to the frontend.

## Vercel deployment

Deploy `frontend/` as a Vite project with `npm run build` and output directory `dist`. Deploy `backend/` as a separate Vercel project; `backend/api/index.py` exposes the FastAPI application as the serverless entrypoint. Set `DATABASE_URL` and `FRONTEND_ORIGIN` only in the backend project, and set `VITE_API_URL` only in the frontend project.
