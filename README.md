# Finance Tracker API

REST API for tracking personal income and expenses.

## Tech Stack

- **FastAPI** — web framework
- **PostgreSQL** — database
- **SQLAlchemy 2.0** — async ORM
- **Alembic** — database migrations
- **JWT** — authentication (access + refresh tokens)
- **Pydantic v2** — data validation

## Features

- User registration and authentication (JWT)
- Categories (income / expense)
- Tags for transactions
- Full CRUD for transactions with filtering
- Monthly statistics by categories
- Yearly summary

## Project Structure

```
app/
├── models/         # SQLAlchemy ORM models
├── schemas/        # Pydantic schemas (request/response)
├── routers/        # API route handlers
├── services/       # Business logic (auth, stats)
└── dependencies/   # FastAPI dependencies (auth guard)
alembic/            # Database migrations
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register` | Register new user |
| POST | `/auth/login` | Login, get tokens |
| POST | `/auth/refresh` | Refresh access token |
| GET | `/users/me` | Get current user |
| PATCH | `/users/me` | Update profile |
| DELETE | `/users/me` | Delete account |
| GET/POST | `/categories/` | List / create categories |
| GET/PATCH/DELETE | `/categories/{id}` | Get / update / delete category |
| GET/POST | `/tags/` | List / create tags |
| GET/PATCH/DELETE | `/tags/{id}` | Get / update / delete tag |
| GET/POST | `/transactions/` | List (with filters) / create |
| GET/PATCH/DELETE | `/transactions/{id}` | Get / update / delete |
| GET | `/stats/monthly` | Monthly stats by categories |
| GET | `/stats/yearly` | Yearly summary |

## Setup

### 1. Clone and install dependencies

```bash
git clone <repo-url>
cd pet_project
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
# Edit .env with your database credentials and secret key
```

### 3. Create database

```sql
CREATE DATABASE finance_tracker;
```

### 4. Run migrations

```bash
alembic revision --autogenerate -m "initial"
alembic upgrade head
```

### 5. Start the server

```bash
python main.py
# or
uvicorn app.main:app --reload
```

Open **http://localhost:8000/docs** for interactive API documentation.

## Example Usage

```bash
# Register
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "username": "john", "password": "secret123"}'

# Login
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "username": "john", "password": "secret123"}'

# Create transaction (use access_token from login)
curl -X POST http://localhost:8000/transactions/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"amount": 5000.00, "type": "income", "date": "2026-04-15", "description": "Salary"}'

# Monthly stats
curl http://localhost:8000/stats/monthly?year=2026&month=4 \
  -H "Authorization: Bearer <access_token>"
```
