from sqlalchemy import text
from dataclasses import dataclass

from config.database import engine


@dataclass
class HealthStatus:
    healthy: bool
    error: str | None = None


async def check_db_health() -> HealthStatus:
    try:
        async with engine.connect() as connection:
            await connection.execute(text("SELECT 1"))
        return HealthStatus(healthy=True)
    except Exception as err:
        return HealthStatus(healthy=False, error=str(err))
