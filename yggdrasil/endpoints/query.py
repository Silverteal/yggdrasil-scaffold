# coding=utf-8
"""注册 Yggdrasil API 的查询端点"""
from typing import Annotated, Optional

from Crypto.PublicKey.RSA import RsaKey
from fastapi import APIRouter, Depends, Response

from yggdrasil.endpoints import handlers
from adofai import GameProfile, SerializedProfile

query_endpoints = APIRouter()  # 实际上是两类 Vanilla API 的整合，所以前缀不固定


@query_endpoints.get("/sessionserver/session/minecraft/profile/{uuid}")
async def from_uuid(rsp: Response,
                    result: Annotated[Optional[GameProfile], Depends(handlers.query.from_uuid)],
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
async def from_name_batch(result: Annotated[
    list[GameProfile], Depends(handlers.query.from_name_batch)
]) -> list[SerializedProfile]:
    """从用户名批量查询用户的UUID"""
    # TODO：安全提示：为防止 CC 攻击，需要为单次查询的角色数目设置最大值，该值至少为 2。
    return [i.serialize("minimum") for i in result]
