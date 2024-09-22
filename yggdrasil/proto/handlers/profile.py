# coding=utf-8
from abc import ABC, abstractmethod
from typing import Literal

from yggdrasil.proto.interfaces.profile import AuthorizationHeader, UploadTexture
from yggdrasil.proto.typealias import GameId


class AbstractProfileApiHandler(ABC):
    """材质管理 API Handler"""

    @abstractmethod
    async def upload(self, *, accessToken: AuthorizationHeader, uuid: GameId,
                     textureType: Literal["skin", "cape"],
                     texture: UploadTexture) -> None:
        raise NotImplementedError

    @abstractmethod
    async def remove(self, *, accessToken: AuthorizationHeader, uuid: GameId,
                     textureType: Literal["skin", "cape"]) -> None:
        raise NotImplementedError
