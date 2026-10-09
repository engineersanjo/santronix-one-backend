"""Request ID middleware for support and audit correlation."""

from uuid import uuid4

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response


class RequestIDMiddleware(BaseHTTPMiddleware):
    """Attach a request ID to every response; do not trust arbitrary IDs blindly."""

    async def dispatch(self, request: Request, call_next) -> Response:
        request_id = request.headers.get("X-Request-ID", "").strip()
        # Accept only short, printable correlation IDs. Otherwise generate one.
        if not request_id or len(request_id) > 100 or not request_id.isascii() or not request_id.isprintable():
            request_id = str(uuid4())
        request.state.request_id = request_id
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response
