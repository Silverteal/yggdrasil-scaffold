# coding=utf-8
from typing import override

from yggdrasil.proto.handlers.query import AbstractQueryApiHandler
from yggdrasil.proto.profiles import GameProfile
from yggdrasil.proto.typealias import GameId
from yggdrasil.pseudo.profiles import pseudo_game_profile


class PseudoHandler(AbstractQueryApiHandler):
    @override
    async def from_uuid(self, *, uuid: GameId) -> GameProfile:
        return pseudo_game_profile()

    @override
    async def from_name_batch(self, *, names: list[str]) -> list[GameProfile]:
        return [pseudo_game_profile() for _ in names]