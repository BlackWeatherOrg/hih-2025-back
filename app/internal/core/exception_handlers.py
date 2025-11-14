from sys import getsizeof

from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi.utils import is_body_allowed_for_status_code
from starlette.exceptions import HTTPException
from starlette.responses import Response
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from internal.core.exceptions import AppException, UnknownException
from internal.core.logs.helpers import exc_to_log, log_requests
from internal.core.utils import calculate_duration


async def unknown_exception_handler(request, exc) -> Response:
    exc = UnknownException()

    body = {'errors': [{'code': exc.full_code(), 'name': exc.__class__.__name__, 'message': exc.msg, 'id': str(exc.uuid), 'value': exc.value}]}
    duration = calculate_duration(request.state.start_time)

    exc_to_log(
        request,
        method=request.method,
        status=exc.status_code,
        route=request.url.path,
        resp_size=getsizeof(body),
        duration=duration)

    return JSONResponse(content=body, status_code=exc.status_code)


async def app_exception_handler(request: Request, exc: AppException):
    body = {'errors': [{'code': exc.full_code(), 'name': exc.__class__.__name__, 'message': exc.msg, 'id': str(exc.uuid), 'value': exc.value}]}
    duration = calculate_duration(request.state.start_time)

    exc_to_log(
        request,
        method=request.method,
        status=exc.status_code,
        route=request.url.path,
        resp_size=getsizeof(body),
        duration=duration)

    raise HTTPException(status_code=exc.status_code, detail=exc.msg)


async def http_exception_handler(request: Request, exc: HTTPException):
    headers = getattr(exc, 'headers', None)
    if not is_body_allowed_for_status_code(exc.status_code):
        return Response(status_code=exc.status_code, headers=headers)
    return JSONResponse({'detail': exc.detail}, status_code=exc.status_code, headers=headers)


async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
    duration = calculate_duration(request.state.start_time)
    exc_to_log(
        request,
        method=request.method,
        status=422,
        route=request.url.path,
        resp_size=getsizeof(exc.errors()),
        duration=duration)

    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content={'detail': jsonable_encoder(exc.errors())},
    )
