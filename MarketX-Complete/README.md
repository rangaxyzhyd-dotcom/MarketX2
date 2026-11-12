# MarketX — Buy Nearby. Sell Everywhere.

A full-stack marketplace starter built from the supplied MarketX visual reference.

## Stack
- Frontend: React 18, Vite, React Router, plain CSS
- Backend: Python 3.11+, FastAPI, SQLAlchemy 2, SQLite by default
- Auth: JWT bearer tokens with hashed passwords
- Listings: create, browse, search, filter by category/location, view details, edit/delete own listings
- Contact seller: seller contact details shown on listing detail
- Images: upload listing photos to backend static storage
- Seed data: optional demo listings

## Run locally

### 1. Backend
```bash
cd backend
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # Windows: copy .env.example .env
uvicorn app.main:app --reload
```
API docs: http://127.0.0.1:8000/docs

### 2. Frontend (new terminal)
```bash
cd frontend
npm install
npm run dev
```
Open http://localhost:5173

The frontend uses `VITE_API_URL` from `.env` and defaults to `http://127.0.0.1:8000`.

## Demo
Register a new account, sign in, then post an ad. You can also seed demo listings:
```bash
cd backend
python -m app.seed
```
Demo users:
- `demo@marketx.in` / `MarketX@123`
- `seller@marketx.in` / `MarketX@123`

## Environment
Copy `backend/.env.example` to `backend/.env`. Change `SECRET_KEY` before deployment.
For production, set a managed PostgreSQL `DATABASE_URL`, configure `CORS_ORIGINS`, and serve uploaded media from object storage/CDN. Do not use SQLite or the sample secret for a public production deployment.

## API highlights
- `POST /api/auth/register`, `POST /api/auth/login`, `GET /api/auth/me`
- `GET /api/categories`
- `GET /api/listings`, `POST /api/listings`, `GET /api/listings/{id}`
- `PATCH /api/listings/{id}`, `DELETE /api/listings/{id}`
- `POST /api/listings/{id}/favorite`, `GET /api/favorites`
- `GET /api/health`

## Notes
This is a runnable, end-to-end marketplace foundation, not a payment escrow or identity-verification platform. For a real launch, add moderation, rate limiting, email/SMS verification, audit logs, image scanning, backups, monitoring, and legal/privacy pages.
