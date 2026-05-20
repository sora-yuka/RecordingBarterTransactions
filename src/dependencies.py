from typing import Annotated

from fastapi import Depends

from src.config.database import AsyncSession, get_session

SessionDep = Annotated[AsyncSession, Depends(get_session)]
