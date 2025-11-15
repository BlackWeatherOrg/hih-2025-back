from typing import Annotated

from fastapi import Depends

from internal.repositories.application import ApplicationRepository
from internal.services.application import ApplicationService


ApplicationRepositoryDependency = Annotated[ApplicationRepository, Depends(ApplicationRepository)]


def application_service_dep(repo: ApplicationRepositoryDependency):
    return ApplicationService(repo=repo)

