# coding=utf-8
__all__ = ["ClientIP"]

from typing import Annotated

from fastapi import Depends, Request


async def get_client_ip(req: Request) -> str:
    """获取客户端连接IP"""
    return req.client.host


ClientIP = Annotated[str, Depends(get_client_ip)]
