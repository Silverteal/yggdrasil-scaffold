# coding=utf-8
"""注册 Yggdrasil API 的材质管理端点"""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from yggdrasil.endpoints import handlers

profile_endpoints = APIRouter(prefix="/api/user/profile")


@profile_endpoints.put("/{uuid}/{textureType}", status_code=204)
async def upload(result: Annotated[bool, Depends(handlers.profile.upload)]) -> None:
    """处理材质上传逻辑。TODO：拒绝不正确的content_type"""
    if not result:
        raise HTTPException(status_code=401)


@profile_endpoints.delete("/{uuid}/{textureType}", status_code=204)
async def remove(result: Annotated[bool, Depends(handlers.profile.remove)]) -> None:
    """处理材质删除逻辑"""
    if not result:
        raise HTTPException(status_code=401)
