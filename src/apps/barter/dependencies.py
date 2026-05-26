from typing import Annotated

from fastapi import Depends

from src.dependencies import SessionDep
from src.apps.auth.dependencies import CurrentUserDep
from src.apps.barter.repositories import BarterRepository

# import service
# import schemas
# if there is util helpers, import them


def get_repository(session: SessionDep):
    return BarterRepository(session)

RepositoryDep = Annotated[BarterRepository, Depends(get_repository)]
