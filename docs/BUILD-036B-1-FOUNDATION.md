# BUILD-036B.1 — FastAPI Foundation

## Purpose

Create a small, runnable API foundation for SANTRONIX ONE. This stage is deliberately limited to service configuration, request correlation, health/readiness, consistent HTTP errors, and automated tests.

## Current endpoints

- `GET /` — service metadata
- `GET /api/v1/health` — process liveness only
- `GET /api/v1/ready` — scaffold readiness and explicit dependency configuration status
- `GET /docs` — interactive OpenAPI documentation in development

## Important limits

At this stage, PostgreSQL, Redis, EMQX/MQTT, authentication, tenant isolation, telemetry persistence, and command execution are **not configured**. The readiness response labels those dependencies accordingly. Do not connect this scaffold to live equipment or treat it as a production control plane.

## Engineering invariants

1. Authentication must establish the actor; clients must not choose their own trusted identity.
2. Every data query must be tenant-scoped before customer data is introduced.
3. A broker acknowledgement is not proof of device execution.
4. A device execution acknowledgement is not verification; verification needs trusted feedback.
5. HTTP `202 Accepted` for future command APIs will mean accepted for asynchronous processing only.
6. Expired or stale commands must not be replayed blindly after an edge reconnects.
7. Secrets belong in environment variables or a managed secret store, never in Git.

## Local acceptance checks

From the repository root, activate the virtual environment and run:

```powershell
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
python -m pytest
python -m uvicorn app.main:app --reload
```

Then open `http://127.0.0.1:8000/docs` and request `/api/v1/health` and `/api/v1/ready`.
