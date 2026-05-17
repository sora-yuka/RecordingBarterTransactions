import uvicorn
from fastapi import FastAPI

from config.settings import settings
from utils.db_health_check import check_db_health


app = FastAPI()

@app.get("/health")
async def health_check():
    status = await check_db_health()
    return {
        "status": "ok" if status.healthy else "degraded",
        "db": {
            "connected": status.healthy,
            "error": status.error
        }
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=True,
    )