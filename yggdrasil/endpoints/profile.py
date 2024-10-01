# coding=utf-8

from fastapi import APIRouter, Depends, Response

from yggdrasil.app import handlers

profile_apis = APIRouter(prefix="/api/user/profile")


@profile_apis.put("/{uuid}/{textureType}", dependencies=[Depends(handlers.profile.upload)], status_code=204)
async def upload() -> None:
    """处理材质上传逻辑。TODO：拒绝不正确的content_type"""
    # 由于不需要返回值，所以此处什么都不用做


@profile_apis.delete("/{uuid}/{textureType}", dependencies=[Depends(handlers.profile.remove)], status_code=204)
async def remove() -> Response:
    """处理材质删除逻辑"""
    # 由于不需要返回值，所以此处什么都不用做
