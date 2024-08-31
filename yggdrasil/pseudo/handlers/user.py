# coding=utf-8
from typing import override
from uuid import uuid4

from yggdrasil.proto.handlers.user import AbstractUserApiHandler, UserApiResponse
from yggdrasil.proto.profiles import GameProfile
from yggdrasil.proto.typealias import AccessToken, ClientToken, UserLoginName
from yggdrasil.pseudo.profiles import pseudo_user_profile
from yggdrasil.util import uuid_to_str


class PseudoUserApiHandler(AbstractUserApiHandler):
    """后续将用户处理类引入"""

    @override
    async def login(self, username: UserLoginName, password: str, clientToken: ClientToken | None,
                    requestUser: bool) -> UserApiResponse:
        """占位"""
        return UserApiResponse(accessToken=AccessToken(password),
                               clientToken=clientToken or uuid_to_str(uuid4()),
                               availableProfiles=[],
                               user=pseudo_user_profile()
                               )

    @override
    async def refresh(self, accessToken: AccessToken, clientToken: ClientToken | None,
                      requestUser: bool, selectedProfile: GameProfile | None) -> UserApiResponse:
        """占位"""
        return UserApiResponse(accessToken=accessToken,
                               clientToken=clientToken or uuid_to_str(uuid4()),
                               selectedProfile=selectedProfile,
                               user=pseudo_user_profile()
                               )

    @override
    async def validate(self, accessToken: AccessToken, clientToken: ClientToken | None) -> bool:
        """占位"""
        return False

    @override
    async def invalidate(self, accessToken: AccessToken) -> None:
        """占位"""
        ...

    @override
    async def logout(self, username: UserLoginName, password: str) -> bool:
        """占位"""
        return False
