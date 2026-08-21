import structlog
from starlette.middleware.base import BaseHTTPMiddleware

logger = structlog.get_logger(__name__)


class GatewayMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        logger.info(f'{request.method} {request.url} {request.headers}')

        response = await call_next(request)

        return response
