# coding=utf-8

__all__ = ["request", "response", "flow_ctx_service"]

from contextvars import ContextVar

from fastapi.requests import Request
from fastapi.responses import Response
from werkzeug.local import LocalProxy

_cv_request: ContextVar[Request] = ContextVar('_cv_request')
_cv_response: ContextVar[Response] = ContextVar('_cv_response')


async def flow_ctx_service(req: Request, rsp: Response) -> None:
    """FastAPI 依赖项，将传入请求存入协程的上下文变量中"""
    global _cv_request, _cv_response
    _cv_request.set(req)
    _cv_response.set(rsp)


request = LocalProxy(_cv_request)
response = LocalProxy(_cv_response)
