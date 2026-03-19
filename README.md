# PhantomGuard 2.0

PhantomGuard 2.0 is a full-stack cybersecurity demo system for monitoring host activity, detecting suspicious behavior, and visualizing alerts in a dark futuristic dashboard.

It contains:

- `frontend/`: React + Vite dashboard
- `backend/`: FastAPI API with auth, alerts, logs, and stats
- `agent/`: Python monitoring agent

## What It Does

PhantomGuard combines three parts:

1. The **agent** monitors local system activity.
2. The **backend** receives logs and stores alerts/statistics.
3. The **frontend** displays login, dashboard, alerts, analytics, and flow visualization.

Detection is currently a hybrid of:

- rule-based anomaly checks
- honeyfile monitoring
- optional BiLSTM model support when the model stack is available

## Architecture

```text
Browser UI (React/Vite)
        |
        v
FastAPI Backend
        |
        v
Python Monitoring Agent
        |
        v
Local system activity, files, processes, anomaly signals
```

## Project Structure

```text
PhantomGuard/
├── frontend/              React dashboard
├── backend/               FastAPI server
├── agent/                 Python monitoring agent
├── model/                 Model artifacts / training assets
├── data/                  Local data and logs
├── design/                Design references
├── specs/                 Supporting specs
├── FINAL_PhantomGuard_OpenSpec.md
├── task.md
├── run_backend.py
├── run_agent.py
├── run_frontend.bat
└── setup_dev.bat
```

## Requirements

- Windows
- Python 3.7+
- Node.js 20+
- npm

## First-Time Setup

### Backend

```powershell
cd d:\Phantomguard\backend
python -m venv venv
venv\Scripts\python.exe -m pip install -r requirements.txt
```

### Frontend

```powershell
cd d:\Phantomguard\frontend
npm install
```

### Agent

```powershell
cd d:\Phantomguard\agent
python -m venv venv
venv\Scripts\python.exe -m pip install -r requirements.txt
```

## How To Run

Run these in separate terminals from the repo root:

### Backend

```powershell
python run_backend.py
```

Backend URLs:

- API root: `http://localhost:8000`
- Health: `http://localhost:8000/health`
- Swagger docs: `http://localhost:8000/docs`

### Frontend

```powershell
run_frontend.bat
```

Frontend URL:

- `http://localhost:5173`

### Agent

```powershell
python run_agent.py
```

## Recommended Local Flow

Use this order:

1. Start the backend.
2. Start the frontend.
3. Start the agent.
4. Open `http://localhost:5173`.
5. Register a new user.
6. Log in.
7. Watch dashboard, alerts, analytics, and flow pages.

## Functional Flow

### Authentication Flow

1. User opens the frontend.
2. User registers through `POST /api/v1/auth/register`.
3. User logs in through `POST /api/v1/auth/login`.
4. Frontend stores the JWT token locally.
5. Protected routes become accessible.

### Monitoring Flow

1. Agent starts collecting file/process/system data.
2. Agent runs anomaly detection.
3. Agent sends logs and alerts to backend endpoints.
4. Backend stores them in SQLite.
5. Frontend fetches:
   - stats from `GET /api/v1/stats/`
   - alerts from `GET /api/v1/alerts/`
   - logs from `GET /api/v1/logs/`
6. Dashboard updates with current system state.

### UI Pages

- `/login`: sign in
- `/register`: create account
- `/dashboard`: summary cards, recent logs, latest alerts
- `/alerts`: alert table with filter/search
- `/analytics`: metrics and trend panels
- `/flow`: system pipeline explanation

## API Summary

### Auth

- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`

### Data

- `GET /api/v1/stats/`
- `GET /api/v1/alerts/`
- `POST /api/v1/alerts/`
- `GET /api/v1/logs/`
- `POST /api/v1/logs/`

## Current Frontend Style

The frontend uses a **Cyber-Modern (Dark Futuristic UI)** style:

- dark layered background
- neon cyan / green highlights
- futuristic typography
- HUD-like panels
- high-contrast dashboard cards

## Notes About The Agent

- The agent currently runs even if the BiLSTM stack is not installed.
- In that case it falls back to rule-based detection.
- On Windows, some monitored folders may produce permission warnings depending on where the process is launched.

## Troubleshooting

### Frontend says "Failed to fetch"

Use:

- frontend: `http://localhost:5173`
- backend: `http://localhost:8000`

Do not use Live Preview or random preview ports when testing login/API flow.

If needed:

```powershell
python run_backend.py
run_frontend.bat
```

### Site cannot be reached

Check that the ports are actually listening:

```powershell
netstat -ano | Select-String ":5173|:8000"
```

### Frontend not updating after code changes

Restart Vite:

```powershell
cd d:\Phantomguard\frontend
npm.cmd run dev -- --host 0.0.0.0 --port 5173
```

### Backend docs not opening

Make sure the backend is running, then open:

```text
http://localhost:8000/docs
```

## Development References

- Spec: [FINAL_PhantomGuard_OpenSpec.md](./FINAL_PhantomGuard_OpenSpec.md)
- Task breakdown: [task.md](./task.md)

## Status

Current repo status:

- backend: runnable
- frontend: runnable
- agent: runnable
- auth flow: wired
- dashboard pages: wired to backend APIs

Some features are still demo-grade and can be extended further, especially deeper real-time streaming, alert actions, and full production hardening.
