# SANTRONIX ONE Backend

Initial FastAPI foundation for the vendor-neutral SANTRONIX ONE infrastructure coordination API.

> **Status: foundation scaffold only.** PostgreSQL, Redis, EMQX/MQTT, authentication, tenant isolation, telemetry persistence, and physical command execution are not configured. Do not connect this scaffold to live equipment or use it as a production control plane.

## Requirements

- Python 3.11 or newer
- Windows PowerShell, macOS, or Linux
- Git

## Windows PowerShell quick start

Clone the repository and enter its folder:

```powershell
git clone https://github.com/engineersanjo/santronix-one-backend.git
cd santronix-one-backend
git switch build-036b1-fastapi-scaffold
```

Create and activate a virtual environment:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
Copy-Item .env.example .env
```

If PowerShell cannot find `py -3.11`, install Python 3.11+ and select the matching interpreter. If local script policy prevents activation, use the appropriate approved local setup for your machine rather than changing system-wide policy.

Run the automated tests:

```powershell
python -m pytest
```

Start the API:

```powershell
python -m uvicorn app.main:app --reload
```

Open the interactive API documentation at http://127.0.0.1:8000/docs.

## Initial endpoints

| Method | Path | Purpose |
| --- | --- | --- |
| GET | `/` | Service metadata |
| GET | `/api/v1/health` | Process liveness |
| GET | `/api/v1/ready` | Scaffold readiness and dependency status |
| GET | `/docs` | OpenAPI docs |

All API routes are currently under `/api/v1/`. Error responses include a request ID to help correlate logs and support reports.

## Architecture and safety boundary

The planned platform coordinates heterogeneous OEM systems rather than replacing their native controllers. Future live commands must pass authenticated identity, tenant-scoped authorization, policy and safety checks, edge/controller acceptance, and independent feedback verification. An HTTP success or broker acknowledgement alone is not proof of physical execution.

Read [the BUILD-036B.1 foundation notes](docs/BUILD-036B-1-FOUNDATION.md) for the current scope and acceptance checks.
