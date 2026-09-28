# Task Management API

FastAPI backend for the task-management application, with JWT authentication, PostgreSQL, Alembic migrations, CORS, email configuration, and an optional ML inference adapter.

## 1. Setup

Create a virtual environment and install dependencies:

```bash
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
# macOS/Linux
source .venv/bin/activate
pip install -r requirement.txt
```

A local-development `.env` is included so the app can import immediately. **Before real use, edit `.env` and replace `DB_CONNECTION` with your PostgreSQL credentials and `SECRET_KEY` with a strong random value. Never commit `.env` to Git. `.env.example` is the shareable template.

## 2. Database

Make sure PostgreSQL is running and the database named in `DB_CONNECTION` exists.

For a fresh database:

```bash
alembic upgrade head
```

This project intentionally does **not** call `Base.metadata.create_all()` at application startup. Database schema changes should go through Alembic.

> If you already have a production/important database created by the old version, take a backup before applying these rewritten migrations. The included migration history is designed for a fresh setup; an existing database may need a one-off migration instead.

## 3. Start the API

```bash
uvicorn main:app --reload
```

Useful URLs:

- API: `http://localhost:8000`
- Swagger: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- Health: `http://localhost:8000/health`

## 4. Frontend integration

The frontend can call these endpoints:

### Authentication

`POST /user/register`

```json
{
  "name": "Ritesh",
  "username": "ritesh",
  "password": "strongpassword",
  "email": "user@example.com"
}
```

`POST /user/login`

Response:

```json
{
  "access_token": "...",
  "token_type": "bearer"
}
```

Send the token on protected requests:

```text
Authorization: Bearer <access_token>
```

### Tasks

- `POST /tasks/create`
- `GET /tasks/all_tasks`
- `GET /tasks/one_task/{task_id}`
- `PUT /tasks/update_task/{task_id}`
- `DELETE /tasks/delete_task/{task_id}`

### CORS

Set `CORS_ORIGINS` in `.env`, for example:

```env
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

Use the real deployed frontend URL in production.

## 5. ML model integration

The ML layer is deliberately optional so the backend works without an ML model.

Set:

```env
ML_ENABLED=true
ML_MODEL_PATH=models/model.joblib
```

Install `joblib` if using a joblib model:

```bash
pip install joblib
```

Place the model at the configured path. The model must expose a `predict(...)` method compatible with:

```python
model.predict([features])
```

Endpoints:

- `GET /ml/health`
- `POST /ml/predict`

Example request:

```json
{
  "features": [1.2, 3.4, 5.6]
}
```

Example response:

```json
{
  "prediction": 0
}
```

The exact feature order and shape must match the model that your ML teammate trained. If the model needs preprocessing, scalers, encoders, or a custom pipeline, package them with the model/pipeline rather than duplicating preprocessing in the frontend.

## 6. Team handoff

Backend owner:
- FastAPI endpoints
- database and migrations
- authentication
- ML inference endpoint
- environment configuration

Frontend owner:
- UI/UX
- React/Next/Vue/etc.
- calls the documented API endpoints
- stores/uses the access token securely according to the frontend architecture

Both:
- agree on JSON request/response shapes
- agree on error handling
- use the same development API base URL
- keep secrets out of Git

## 7. Security checklist

- Never commit `.env`.
- Rotate any credentials that were previously committed/shared.
- Use a strong unique `SECRET_KEY` in production.
- Restrict `CORS_ORIGINS` to the actual frontend domain(s).
- Use HTTPS in production.
- Do not load an untrusted pickle/joblib model.
