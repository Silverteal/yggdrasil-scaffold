# coding=utf-8
"""注册 Yggdrasil API 的查询端点"""
from typing import Annotated, Optional

from Crypto.PublicKey.RSA import RsaKey
from adofai import SerializedProfile
from adofai.models import FulfilledGameProfile, PartialGameProfile
from fastapi import APIRouter, Depends, Response

from yggdrasil.endpoints import handlers

query_endpoints = APIRouter()  # 实际上是两类 Vanilla API 的整合，所以前缀不固定


@query_endpoints.get("/sessionserver/session/minecraft/profile/{uuid}")
async def query_by_uuid(rsp: Response,
                        result: Annotated[FulfilledGameProfile | None, Depends(handlers.query.query_by_uuid)],
                        sign_key: Annotated[RsaKey, Depends(handlers.root.sign_key)],
                        unsigned: bool = True) -> SerializedProfile | None:
    """从UUID查询单个玩家"""
    if result is not None:
        if unsigned:
            return result.serialize("unsigned")
        else:
            return result.serialize("full", sign_key)
    else:
        rsp.status_code = 204
        return None


@query_endpoints.post("/api/profiles/minecraft")
async def query_by_names(result: Annotated[
    list[PartialGameProfile], Depends(handlers.query.query_by_names)
]) -> list[SerializedProfile]:
    """从用户名批量查询用户的UUID"""
    return [i.serialize("minimum") for i in result]
