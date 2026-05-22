import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.config.settings import settings
from src.utils.db_health_check import check_db_health
from src.apps.auth.routers import router as user_router

app = FastAPI()

app.mount("/media", StaticFiles(directory="media"), name="media")


@app.get("/health")
async def health_check():
    status = await check_db_health()
    return {
        "status": "ok" if status.healthy else "degraded",
        "db": {"connected": status.healthy, "error": status.error},
    }


app.include_router(user_router, prefix="/api/v1/auth", tags=["auth"])


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True,
    )
