# coding=utf-8
from functools import cache
from typing import Literal, Optional, override
from uuid import uuid4

from Crypto.PublicKey import RSA
from Crypto.PublicKey.RSA import RsaKey

from yggdrasil.exceptions import YggdrasilException
from yggdrasil.handlers.proto import *
from adofai.profiles import GameProfile
from adofai import AccessToken, GameId
from yggdrasil.models.root import MetaData
from yggdrasil.models.session import JoinRequest
from yggdrasil.models.user import LoginRequest, LogoutRequest, RefreshRequest, UserEndpointsResponse, ValidationsRequest
from yggdrasil.test.pseudo.profiles import pseudo_game_profile, pseudo_user_profile
from yggdrasil.utils.context import AuthorizationHeader, ClientIP, UploadTexture
from adofai.utils.uuid import uuid_to_str


class PseudoHandlerProfile(AbstractHandlerProfile):

    async def upload(self, *, accessToken: AuthorizationHeader, uuid: GameId,
                     textureType: Literal["skin", "cape"],
                     texture: UploadTexture) -> bool:
        if not accessToken:
            return False
        if texture.content_type != "image/png":
            raise YggdrasilException(418, "NoWay", f"What a `nice` {textureType}!")
        return True

    async def remove(self, *, accessToken: AuthorizationHeader, uuid: GameId,
                     textureType: Literal["skin", "cape"]) -> bool:
        if accessToken:
            return True
        else:
            return False


class PseudoHandlerQuery(AbstractHandlerQuery):
    @override
    async def from_uuid(self, *, uuid: GameId) -> GameProfile | None:
        return pseudo_game_profile()

    @override
    async def from_name_batch(self, *, names: list[str]) -> list[GameProfile]:
        return [pseudo_game_profile() for _ in names]


class PseudoHandlerRoot(AbstractHandlerRoot):
    @override
    async def home(self) -> MetaData:
        return MetaData(meta={}, skinDomains=[])

    @override
    @cache
    def sign_key(self) -> RsaKey:
        return RSA.generate(2048)


class PseudoHandlerSession(AbstractHandlerSession):
    @override
    async def join(self, *, form: JoinRequest, ip: ClientIP) -> bool:
        if len(form.accessToken) > 5:
            return True
        else:
            return False

    @override
    async def has_joined(self, *, username: str, serverId: str, ip: Optional[str] = None) -> GameProfile | None:
        if ip:
            return pseudo_game_profile()
        else:
            return None


class PseudoHandlerUser(AbstractHandlerUser):
    """后续将用户处理类引入"""

    @override
    async def login(self, *, form: LoginRequest) -> UserEndpointsResponse | None:
        """占位"""
        return UserEndpointsResponse(accessToken=AccessToken(form.password),
                                     clientToken=form.clientToken or uuid_to_str(uuid4()),
                                     availableProfiles=[],
                                     user=pseudo_user_profile()
                                     )

    @override
    async def refresh(self, *, form: RefreshRequest) -> UserEndpointsResponse:
        """占位"""
        return UserEndpointsResponse(accessToken=form.accessToken,
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
