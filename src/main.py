import uvicorn
from fastapi import FastAPI

from config.settings import settings


app = FastAPI()


if __name__ == "__main__":
    uvicorn.run(
        app,
        host=settings.host,
        port=settings.port,
        reload=True,
        reload_delay=2
    )