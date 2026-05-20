import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.config.settings import settings
from src.utils.db_health_check import check_db_health

app = FastAPI()

app.mount("/media", StaticFiles(directory="media"), name="media")


@app.get("/health")
async def health_check():
    status = await check_db_health()
    return {
        "status": "ok" if status.healthy else "degraded",
        "db": {"connected": status.healthy, "error": status.error},
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=True,
    )
