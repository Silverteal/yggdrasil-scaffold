# coding=utf-8

__all__ = ["userapis"]

from fastapi import FastAPI, Request
from starlette.exceptions import HTTPException

from yggdrasil.api.server.user import userapis
from proto.exceptions import YggdrasilException, yggdrasil_error_response

app = FastAPI()


# 上下顺序能不能换？
@app.exception_handler(YggdrasilException)
async def yggdrasil_exception_handler(_: Request, exc: YggdrasilException):
    """处理业务异常"""
    return yggdrasil_error_response(exc.status_code,
                                    exc.error,
                                    exc.errorMessage,
                                    exc.cause)


# 上下顺序能不能换？
@app.exception_handler(HTTPException)
async def http_exception_handler(_: Request, exc: HTTPException):
    """处理和转录非业务异常为标准格式"""
    return yggdrasil_error_response(exc.status_code,
                                    "InternalUndefinedException",
                                    "An unexpected error has occurred. Contact site admin for details.",
                                    exc.detail,
                                    exc.headers)


app.include_router(userapis)
