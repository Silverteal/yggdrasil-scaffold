from functools import cache
from typing import Literal, Optional, override
from uuid import uuid4

from Crypto.PublicKey import RSA
from Crypto.PublicKey.RSA import RsaKey
from fastapi import HTTPException

from yggdrasil.exceptions import InvalidToken, YggdrasilException
from yggdrasil.proto.handlers import *
from yggdrasil.proto.interfaces.profile import *
from yggdrasil.proto.interfaces.root import *
from yggdrasil.proto.interfaces.session import JoinRequest
from yggdrasil.proto.interfaces.user import LoginRequest, LogoutRequest, RefreshRequest, UserApiResponse, \
    ValidationsRequest
from yggdrasil.proto.profiles import GameProfile
from yggdrasil.proto.statictypes import AccessToken, GameId
from yggdrasil.test.pseudo.profiles import pseudo_game_profile, pseudo_user_profile
from yggdrasil.utils.context import ClientIP
from yggdrasil.utils.uuid import uuid_to_str


class PseudoProfileApiHandler(AbstractProfileApiHandler):

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


class PseudoQueryApiHandler(AbstractQueryApiHandler):
    @override
    async def from_uuid(self, *, uuid: GameId) -> GameProfile:
        return pseudo_game_profile()

    @override
    async def from_name_batch(self, *, names: list[str]) -> list[GameProfile]:
        return [pseudo_game_profile() for _ in names]


class PseudoRootApiHandler(AbstractRootApiHandler):
    @override
    async def home(self) -> MetaData:
        return MetaData(meta={}, skinDomains=[])

    @override
    @cache
    def sign_key(self) -> RsaKey:
        return RSA.generate(2048)


class PseudoSessionApiHandler(AbstractSessionApiHandler):
    @override
    async def join(self, *, form: JoinRequest, ip: ClientIP) -> None:
        pass

    @override
    async def has_joined(self, *, username: str, serverId: str, ip: Optional[str] = None) -> GameProfile:
        if ip:
            return pseudo_game_profile()
        else:
            raise InvalidToken


class PseudoUserApiHandler(AbstractUserApiHandler):
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
