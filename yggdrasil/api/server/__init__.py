# coding=utf-8

__all__ = ["userapis"]

from fastapi import Depends, FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.utils import is_body_allowed_for_status_code
from starlette.exceptions import HTTPException
from fastapi.exception_handlers import http_exception_handler

from yggdrasil.api.server.user import userapis
from yggdrasil.api.flow import flow_ctx_service
from yggdrasil.proto.exceptions import YggdrasilException, yggdrasil_error_response

app = FastAPI(dependencies=[Depends(flow_ctx_service)])


@app.exception_handler(RequestValidationError)
async def request_validation_error_adapter(req: Request, exc: RequestValidationError):
    """处理和转录请求格式错误异常为标准格式"""
    return yggdrasil_error_response(status_code=422,
                                    error="RequestValidationError",
                                    errorMessage="The request form has incorrect parameters and can't be processed.",
                                    cause=jsonable_encoder(exc.errors()))


@app.exception_handler(YggdrasilException)
async def yggdrasil_exception_handler(req: Request, exc: YggdrasilException):
    """处理业务异常"""
    if not is_body_allowed_for_status_code(exc.status_code):
        return http_exception_handler(req, exc)
    return yggdrasil_error_response(exc.status_code,
                                    exc.error,
                                    exc.errorMessage,
                                    exc.cause)


@app.exception_handler(HTTPException)
async def http_exception_adapter(req: Request, exc: HTTPException):
    """处理和转录非业务异常为标准格式"""
    if not is_body_allowed_for_status_code(exc.status_code):
        return http_exception_handler(req, exc)
    return yggdrasil_error_response(exc.status_code,
                                    "InternalServerError",
                                    "An internal server error has occurred. Contact site admin for details.",
                                    exc.__repr__(),
                                    exc.headers)


app.include_router(userapis)
