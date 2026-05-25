from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse


class BaseAppException(Exception):
    """Base exception for whole application"""

    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_message = "An unexpected error occured"

    def __init__(self, message: str | None = None):
        self.message = message or self.default_message
        super().__init__(self.message)


def register_exception_handlers(app: FastAPI) -> None:
    """Catch any custom exception and automatically returns its status code"""

    @app.exception_handler(BaseAppException)
    async def app_exception_handler(
        request: Request, exc: BaseAppException
    ) -> JSONResponse:
        return JSONResponse(status_code=exc.status_code, content={"error": exc.message})
