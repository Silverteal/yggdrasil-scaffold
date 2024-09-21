# coding=utf-8
from abc import ABC, abstractmethod
from typing import Optional

from yggdrasil.proto.profiles import GameProfile
from yggdrasil.proto.adapters.session import JoinRequest


class AbstractSessionApiHandler(ABC):
    """正版验证 API Handler"""

    @abstractmethod
    async def join(self, form: JoinRequest) -> None:
        raise NotImplementedError

    @abstractmethod
    async def has_joined(self, username: str, serverId: str, ip: Optional[str] = None) -> GameProfile:
        raise NotImplementedError
