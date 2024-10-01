# coding=utf-8
from typing import Annotated

from Crypto.PublicKey.RSA import RsaKey
from fastapi import APIRouter, Depends, Response

from yggdrasil.app import handlers
from yggdrasil.proto.profiles import GameProfile
from yggdrasil.proto.profiles import SerializedProfile

session_apis = APIRouter(prefix="/sessionserver/session/minecraft")


@session_apis.post("/join", dependencies=[Depends(handlers.session.join)], status_code=204)
async def join() -> Response:
    """处理玩家侧正版验证逻辑"""
    # 由于不需要返回值，所以此处什么都不用做


@session_apis.get("/hasJoined")
async def has_joined(game_profile: Annotated[GameProfile, Depends(handlers.session.has_joined)],
                     sign_key: Annotated[RsaKey, Depends(handlers.root.sign_key)]) -> SerializedProfile:
    """处理服务侧正版验证逻辑"""
    return game_profile.serialize("full", sign_key)
