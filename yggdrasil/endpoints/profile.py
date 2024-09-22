# coding=utf-8

from fastapi import APIRouter, Depends
from fastapi.responses import Response

from yggdrasil.apphandlers.profile import handler

profileapis = APIRouter(prefix="/api/user/profile")


@profileapis.put("/{uuid}/{textureType}", dependencies=[Depends(handler.upload)])
async def upload() -> Response:
    """处理材质上传逻辑。TODO：拒绝不正确的content_type"""
    return Response(status_code=204)


@profileapis.delete("/{uuid}/{textureType}", dependencies=[Depends(handler.remove)])
async def remove() -> Response:
    """处理材质删除逻辑"""
    return Response(status_code=204)
