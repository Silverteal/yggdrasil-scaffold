# coding=utf-8
from typing import override
from uuid import uuid4

from yggdrasil.proto.interfaces.user import *
from yggdrasil.proto.handlers.user import AbstractUserApiHandler
from yggdrasil.proto.typealias import AccessToken
from yggdrasil.pseudo.profiles import pseudo_user_profile
from yggdrasil.util import uuid_to_str


class PseudoHandler(AbstractUserApiHandler):
    """后续将用户处理类引入"""

    @override
    async def login(self, *, form: LoginRequest) -> UserApiResponse:
        """占位"""
        return UserApiResponse(accessToken=AccessToken(form.password),
                               clientToken=form.clientToken or uuid_to_str(uuid4()),
                               availableProfiles=[],
                               user=pseudo_user_profile()
                               )

    @override
    async def refresh(self, *, form: RefreshRequest) -> UserApiResponse:
        """占位"""
        return UserApiResponse(accessToken=form.accessToken,
                               clientToken=form.clientToken or uuid_to_str(uuid4()),
                               selectedProfile=form.selectedProfile,
                               user=pseudo_user_profile()
                               )

    @override
    async def validate(self, *, _: ValidationsRequest) -> bool:
        """占位"""
        return False

    @override
    async def invalidate(self, *, _: ValidationsRequest) -> None:
        """占位"""

    @override
    async def logout(self, *, _: LogoutRequest) -> bool:
        """占位"""
        return False
