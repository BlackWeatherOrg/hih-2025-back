from typing import Annotated

from fastapi import APIRouter, Depends

from internal.dependencies.application import application_service_dep
from internal.dto.application import (
    ApplicationOut,
    CreateApplicationDTO,
    GetApplicationDTO,
    UpdateApplicationDTO,
)
from internal.services.application import ApplicationService


APPLICATION_ROUTER = APIRouter(prefix='/applications', tags=['applications'])


@APPLICATION_ROUTER.get('/get_one', response_model=ApplicationOut)
async def get_one_application(
    request_data: Annotated[GetApplicationDTO, Depends(GetApplicationDTO)],
    service: ApplicationService = Depends(application_service_dep),
):
    return await service.get_one(request_data)


@APPLICATION_ROUTER.get('/get_many', response_model=list[ApplicationOut])
async def get_many_applications(
    request_data: Annotated[GetApplicationDTO, Depends(GetApplicationDTO)],
    service: ApplicationService = Depends(application_service_dep),
):
    return await service.get_many(request_data)


@APPLICATION_ROUTER.post('/create', response_model=ApplicationOut)
async def create_application(
    request_data: CreateApplicationDTO,
    service: ApplicationService = Depends(application_service_dep),
):
    return await service.create(request_data)


@APPLICATION_ROUTER.patch('/update', response_model=ApplicationOut)
async def update_application(
    application_id: int,
    request_data: UpdateApplicationDTO,
    service: ApplicationService = Depends(application_service_dep),
):
    return await service.update(application_id, request_data)


@APPLICATION_ROUTER.delete('/delete')
async def delete_application(
    application_id: int,
    service: ApplicationService = Depends(application_service_dep),
):
    await service.delete(application_id)
    return {'status_code': 204, 'message': 'deleted'}

