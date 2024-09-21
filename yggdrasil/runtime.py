# coding=utf-8

__all__ = ["request", "response", "common_flow_service", "config"]

from contextvars import ContextVar

from Crypto.PublicKey import RSA
from fastapi import Request, Response
from werkzeug.local import LocalProxy

from yggdrasil.proto.configs import YggdrasilConfig

_cv_request: ContextVar[Request] = ContextVar('_cv_request')
_cv_response: ContextVar[Response] = ContextVar('_cv_response')
config: YggdrasilConfig = YggdrasilConfig(sign_key=RSA.generate(1024))  # TODO


async def common_flow_service(req: Request, rsp: Response) -> None:
    """FastAPI 依赖项，将传入请求存入协程的上下文变量中"""
    global _cv_request, _cv_response, config
    _cv_request.set(req)
    _cv_response.set(rsp)
    # config = _cv_request.get().app.state.yggdrasil_config


request = LocalProxy(_cv_request)
response = LocalProxy(_cv_response)
