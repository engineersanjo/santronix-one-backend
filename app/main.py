"""FastAPI application entry point."""

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.routes import router
from app.core.config import get_settings
from app.core.request_id import RequestIDMiddleware

settings = get_settings()
app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description=(
        "Initial SANTRONIX ONE API foundation. This service does not yet connect to "
        "live equipment, databases, or message brokers."
    ),
)
app.add_middleware(RequestIDMiddleware)
app.include_router(router, prefix=settings.api_v1_prefix)


def _error_body(request: Request, *, code: str, title: str, status: int, detail: object) -> dict[str, object]:
    return {
        "type": "about:blank",
        "title": title,
        "status": status,
        "detail": detail,
        "instance": request.url.path,
        "code": code,
        "request_id": getattr(request.state, "request_id", "unavailable"),
    }


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    titles = {400: "Bad Request", 401: "Unauthorized", 403: "Forbidden", 404: "Not Found", 405: "Method Not Allowed"}
    title = titles.get(exc.status_code, "HTTP Error")
    return JSONResponse(
        status_code=exc.status_code,
        content=_error_body(
            request,
            code=f"HTTP_{exc.status_code}",
            title=title,
            status=exc.status_code,
            detail=exc.detail,
        ),
        headers=exc.headers,
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content=_error_body(
            request,
            code="VALIDATION_ERROR",
            title="Request Validation Failed",
            status=422,
            detail=exc.errors(),
        ),
    )


@app.get("/", include_in_schema=False)
def root() -> dict[str, str]:
    return {"service": settings.app_name, "api": settings.api_v1_prefix, "docs": "/docs"}
