# coding=utf-8
from abc import ABC, abstractmethod

from yggdrasil.proto.profiles import GameProfile
from yggdrasil.proto.typealias import GameId


class AbstractQueryApiHandler(ABC):
    """玩家档案查询 API Handler"""

    @abstractmethod
    async def from_uuid(self, *, uuid: GameId) -> GameProfile:
        raise NotImplementedError

    @abstractmethod
    async def from_name_batch(self, *, names: list[str]) -> list[GameProfile]:
        raise NotImplementedError