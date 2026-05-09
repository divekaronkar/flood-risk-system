# Flood-Risk Detection System (Backend)

## Setup

1. Create MySQL database:

```sql
CREATE DATABASE flood_risk;
```

2. Copy env:

- Copy `.env.example` → `.env`
- Update `DATABASE_URL` and `JWT_SECRET_KEY`

3. Install deps (already in this repo’s `.venv`):

```powershell
.\backend\.venv\Scripts\python.exe -m pip install -r backend\requirements.txt
```

4. Train ML model:

```powershell
.\backend\.venv\Scripts\python.exe backend\scripts\train_model.py
```

5. Seed sample locations + 10-year analytics:

```powershell
.\backend\.venv\Scripts\python.exe backend\scripts\seed_data.py
```

6. Run API:

```powershell
.\backend\.venv\Scripts\uvicorn.exe app.main:app --reload --app-dir backend
```

