from typing import Annotated

from fastapi import Depends

from config.database import AsyncSession, get_session


SessionDep = Annotated[AsyncSession, Depends(get_session)]