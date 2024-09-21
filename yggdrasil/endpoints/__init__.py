# coding=utf-8

__all__ = ["userapis"]

from http import HTTPStatus

from fastapi import Depends, FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exception_handlers import http_exception_handler
from fastapi.exceptions import RequestValidationError
from fastapi.utils import is_body_allowed_for_status_code
from starlette.exceptions import HTTPException

from yggdrasil.runtime import common_flow_service
from yggdrasil.endpoints.session import sessionapis
from yggdrasil.endpoints.user import userapis
from yggdrasil.proto.exceptions import DirectResponseWrapper, YggdrasilException, yggdrasil_error_response

app = FastAPI(dependencies=[Depends(common_flow_service)])


@app.exception_handler(DirectResponseWrapper)
async def not_implemented_adapter(req: Request, exc: DirectResponseWrapper):
    """直接返回响应体"""
    return exc.response


@app.exception_handler(NotImplementedError)
async def not_implemented_adapter(req: Request, exc: NotImplementedError):
    """处理未实现异常"""
    return yggdrasil_error_response(status_code=501,
                                    error="NotImplementedError",
                                    errorMessage="The endpoint you have requested is not implemented."
                                    )


@app.exception_handler(RequestValidationError)
async def request_validation_error_adapter(req: Request, exc: RequestValidationError):
    """处理和转录请求格式错误异常为标准格式"""
    return yggdrasil_error_response(status_code=422,
                                    error="RequestValidationError",
                                    errorMessage="The request has incorrect parameters and can't be processed.",
                                    cause=jsonable_encoder(exc.errors()))


@app.exception_handler(YggdrasilException)
async def yggdrasil_exception_handler(req: Request, exc: YggdrasilException):
    """处理业务异常"""
    if not is_body_allowed_for_status_code(exc.status_code):
        return http_exception_handler(req, exc)
    return yggdrasil_error_response(exc.status_code,
                                    exc.error,
                                    exc.errorMessage,
                                    jsonable_encoder(exc.cause))


@app.exception_handler(HTTPException)
async def http_exception_adapter(req: Request, exc: HTTPException):
    """处理和转录非业务异常为标准格式"""
    if not is_body_allowed_for_status_code(exc.status_code):
        return http_exception_handler(req, exc)
    stc = HTTPStatus(exc.status_code)

    if stc == 418:
        phr = "TeapotAbuse"
    else:
        phr = (stc.phrase
               .replace(' ', '')
               .replace('-', '')
               )
        if stc.is_success or stc.is_redirection:
            phr = "NotError"
    desc = f"HTTP Status: {stc} {stc.phrase}; {stc.description}"
    return yggdrasil_error_response(exc.status_code,
                                    phr,
                                    desc,
                                    exc.detail,
                                    exc.headers)


@app.exception_handler(Exception)
async def exception_adapter(req: Request, exc: Exception):
    """一般运行时错误的处理"""
    return yggdrasil_error_response(500,
                                    "BackendException",
                                    "Backend raised an exception. Check server console.",
                                    )


app.include_router(userapis)
app.include_router(sessionapis)
