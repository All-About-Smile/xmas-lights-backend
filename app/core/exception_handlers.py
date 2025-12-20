from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.exceptions import (
    AppException,
    AuthException,
    ErrorCodes,
    PermissionDeniedException,
)
from app.core.responses import CommonResponse


async def app_exception_handler(request: Request, exc: AppException):
    """
    비즈니스 예외(AppException 계열) -> CommonResponse 형태로 변환
    """
    status = 400

    if isinstance(exc, AuthException):
        status = 401
    elif isinstance(exc, PermissionDeniedException):
        status = 403
    elif exc.code in (ErrorCodes.USER_NOT_FOUND, ErrorCodes.LETTER_NOT_FOUND):
        status = 404

    return JSONResponse(
        status_code=status,
        content=CommonResponse[None](
            code=exc.code,
            message=exc.message,
            data=None,
            meta=exc.meta,
        ).model_dump(),
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content=CommonResponse[None](
            code=ErrorCodes.VALIDATION_ERROR,
            message="Request validation error",
            data=None,
            meta={"errors": exc.errors()},
        ).model_dump(),
    )


async def generic_exception_handler(request: Request, exc: Exception):
    """
    예상치 못한 모든 예외
    """
    return JSONResponse(
        status_code=500,
        content=CommonResponse[None](
            code=ErrorCodes.INTERNAL_ERROR,
            message="Internal Server Error",
            data=None,
        ).model_dump(),
    )
