# coding=utf-8
from typing import Optional, override

from yggdrasil.proto.adapters.session import JoinRequest
from yggdrasil.proto.exceptions import InvalidToken
from yggdrasil.proto.handlers.session import AbstractSessionApiHandler
from yggdrasil.proto.profiles import GameProfile
from yggdrasil.pseudo.profiles import pseudo_game_profile


class PseudoHandler(AbstractSessionApiHandler):
    @override
    async def join(self, form: JoinRequest) -> None:
        pass

    @override
    async def has_joined(self, username: str, serverId: str, ip: Optional[str] = None) -> GameProfile:
        if ip:
            return pseudo_game_profile()
        else:
            raise InvalidToken
