# coding=utf-8
from typing import Annotated, Optional

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse, Response

from yggdrasil.apphandlers.query import handler
from yggdrasil.proto.profiles import GameProfile
from yggdrasil.runtime import config

queryapis = APIRouter()  # 实际上是两类 Vanilla API 的整合，所以前缀不固定


@queryapis.get("/sessionserver/session/minecraft/profile/{uuid}")
async def from_uuid(result: Annotated[Optional[GameProfile], Depends(handler.from_uuid)],
                    unsigned: bool = True) -> Response:
    """从UUID查询单个玩家"""
    if result:
        if unsigned:
            return JSONResponse(result.serialize("unsigned"))
        else:
            return JSONResponse(result.serialize("full", config.sign_key))
    else:
        return Response(status_code=204)


@queryapis.post("/api/profiles/minecraft")
async def from_name_batch(result: Annotated[
    list[GameProfile], Depends(handler.from_name_batch)
]) -> JSONResponse:
    """从用户名批量查询用户的UUID"""
    # TODO：安全提示：为防止 CC 攻击，需要为单次查询的角色数目设置最大值，该值至少为 2。
    return JSONResponse([i.serialize("minimum") for i in result])
