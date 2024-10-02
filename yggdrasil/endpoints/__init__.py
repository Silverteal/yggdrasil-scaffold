# coding=utf-8
"""本包注册了 Yggdrasil API 的 FastAPI 端点，包括相关异常处理流程和默认占位处理程序"""
from http import HTTPStatus

from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exception_handlers import http_exception_handler
from fastapi.exceptions import RequestValidationError
from fastapi.utils import is_body_allowed_for_status_code
from starlette.exceptions import HTTPException

from yggdrasil.endpoints.profile import profile_endpoints
from yggdrasil.endpoints.query import query_endpoints
from yggdrasil.endpoints.root import root_endpoints
from yggdrasil.endpoints.session import session_endpoints
from yggdrasil.endpoints.user import user_endpoints
from yggdrasil.exceptions import DirectResponseWrapper, YggdrasilException, yggdrasil_error_response

fastapi_instance = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)


# TODO：换个地放exception_handler
@fastapi_instance.exception_handler(DirectResponseWrapper)
async def direct_response_adapter(req: Request, exc: DirectResponseWrapper):
    """直接返回响应体"""
    return exc.response


@fastapi_instance.exception_handler(NotImplementedError)
async def not_implemented_adapter(req: Request, exc: NotImplementedError):
    """处理未实现异常"""
    return yggdrasil_error_response(status_code=501,
                                    error="NotImplementedError",
                                    errorMessage="The endpoint you have requested is not implemented.",
                                    )


@fastapi_instance.exception_handler(RequestValidationError)
async def request_validation_error_adapter(req: Request, exc: RequestValidationError):
    """处理和转录请求格式错误异常为标准格式"""
    return yggdrasil_error_response(status_code=422,
                                    error="RequestValidationError",
                                    errorMessage="The request has incorrect parameters and can't be processed.",
                                    cause=jsonable_encoder(exc.errors()),
                                    )


@fastapi_instance.exception_handler(YggdrasilException)
async def yggdrasil_exception_handler(req: Request, exc: YggdrasilException):
    """处理业务异常"""
    if not is_body_allowed_for_status_code(exc.status_code):
        return http_exception_handler(req, exc)
    return yggdrasil_error_response(exc.status_code,
                                    exc.error,
                                    exc.errorMessage,
                                    jsonable_encoder(exc.cause)
                                    )


@fastapi_instance.exception_handler(HTTPException)
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
    desc = f"{stc} {stc.phrase}; {stc.description}"
    cause = exc.detail if exc.detail != stc.phrase else None
    return yggdrasil_error_response(exc.status_code,
                                    phr,
                                    desc,
                                    cause,
                                    exc.headers
                                    )


@fastapi_instance.exception_handler(Exception)
async def exception_adapter(req: Request, exc: Exception):
    """一般运行时错误的处理"""
    return yggdrasil_error_response(500,
                                    "BackendException",
                                    "Backend raised an exception. Check server console.",
                                    )


fastapi_instance.include_router(user_endpoints)
fastapi_instance.include_router(session_endpoints)
fastapi_instance.include_router(query_endpoints)
fastapi_instance.include_router(profile_endpoints)
fastapi_instance.include_router(root_endpoints)
