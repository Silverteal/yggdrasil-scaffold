# coding=utf-8
from typing import Literal

from fastapi import HTTPException

from yggdrasil.proto.exceptions import YggdrasilException
from yggdrasil.proto.handlers.profile import AbstractProfileApiHandler
from yggdrasil.proto.interfaces.profile import AuthorizationHeader, UploadTexture
from yggdrasil.proto.typealias import GameId


class PseudoHandler(AbstractProfileApiHandler):

    async def upload(self, *, accessToken: AuthorizationHeader, uuid: GameId,
                     textureType: Literal["skin", "cape"],
                     texture: UploadTexture) -> None:
        if not accessToken:
            raise HTTPException(401)
        if texture.content_type != "image/png":
            raise YggdrasilException(418, "NoWay", f"What a `nice` {textureType}!")
        return None

    async def remove(self, *, accessToken: AuthorizationHeader, uuid: GameId,
                     textureType: Literal["skin", "cape"]) -> None:
        if not accessToken:
            raise HTTPException(401)
        return None
