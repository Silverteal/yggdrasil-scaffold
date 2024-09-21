# coding=utf-8
from typing import Annotated

from fastapi import APIRouter, Depends, Response
from fastapi.responses import JSONResponse

from yggdrasil.apphandlers.session import handler
from yggdrasil.runtime import config
from yggdrasil.proto.profiles import GameProfile

sessionapis = APIRouter(prefix="/sessionserver/session/minecraft")


@sessionapis.post("/join", dependencies=[Depends(handler.join)])
async def join() -> Response:
    """处理玩家侧正版验证逻辑"""
    return Response(status_code=204)


@sessionapis.get("/hasJoined")
async def has_joined(game_profile: Annotated[GameProfile, Depends(handler.has_joined)]) -> JSONResponse:
    """处理服务侧正版验证逻辑"""
    return JSONResponse(game_profile.serialize("full", config.sign_key))
