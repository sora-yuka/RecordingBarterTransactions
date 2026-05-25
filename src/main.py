import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from src.config.settings import settings
from src.config.exceptions import register_exception_handlers
from src.utils.health_check_handler import check_db_health
from src.apps.auth.routers import router as user_router

app = FastAPI()

register_exception_handlers(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


@app.get("/health")
async def health_check():
    status = await check_db_health()
    return {
        "status": "ok" if status.healthy else "degraded",
        "db": {"connected": status.healthy, "error": status.error},
    }


app.include_router(user_router, prefix="/api/v1/auth", tags=["Auth"])


if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True,
    )
