"""Initial service health routes."""

from fastapi import APIRouter, Request

router = APIRouter()


@router.get("/health", tags=["operations"], summary="Liveness check")
def health(request: Request) -> dict[str, str]:
    """Report that the process can serve requests; does not prove dependencies are ready."""
    return {
        "status": "ok",
        "service": request.app.title,
        "request_id": getattr(request.state, "request_id", "unavailable"),
    }


@router.get("/ready", tags=["operations"], summary="Service readiness check")
def readiness(request: Request) -> dict[str, object]:
    """Report the capabilities available in this scaffold without claiming DB/broker readiness."""
    return {
        "status": "ready",
        "service": request.app.title,
        "stage": "foundation",
        "dependencies": {
            "database": "not_configured",
            "message_broker": "not_configured",
            "authentication": "not_configured",
        },
        "request_id": getattr(request.state, "request_id", "unavailable"),
    }
