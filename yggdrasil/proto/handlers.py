# coding=utf-8
__all__ = ["AbstractProfileApiHandler", "AbstractQueryApiHandler", "AbstractRootApiHandler",
           "AbstractSessionApiHandler", "AbstractUserApiHandler"]

from abc import ABC
from typing import Literal, Optional

from Crypto.PublicKey.RSA import RsaKey

from yggdrasil.proto.interfaces.profile import *
from yggdrasil.proto.interfaces.root import *
from yggdrasil.proto.interfaces.session import JoinRequest
from yggdrasil.proto.interfaces.user import *
from yggdrasil.proto.profiles import GameProfile
from yggdrasil.proto.statictypes import GameId
from yggdrasil.utils.context import ClientIP


class AbstractUserApiHandler(ABC):
    """用户 API Handler"""

    async def login(self, *, form: LoginRequest) -> UserApiResponse | None:
        raise NotImplementedError

    async def refresh(self, *, form: RefreshRequest) -> UserApiResponse:
        raise NotImplementedError

    async def validate(self, *, form: ValidationsRequest) -> bool:
        raise NotImplementedError

    async def invalidate(self, *, form: ValidationsRequest) -> None:
        raise NotImplementedError

    async def logout(self, *, form: LogoutRequest) -> bool:
        raise NotImplementedError


class AbstractSessionApiHandler(ABC):
    """正版验证 API Handler"""

    async def join(self, *, form: JoinRequest, ip: ClientIP) -> None:
        raise NotImplementedError

    async def has_joined(self, *, username: str, serverId: str, ip: Optional[str] = None) -> GameProfile:
        raise NotImplementedError


class AbstractQueryApiHandler(ABC):
    """玩家档案查询 API Handler"""

    async def from_uuid(self, *, uuid: GameId) -> GameProfile:
        raise NotImplementedError

    async def from_name_batch(self, *, names: list[str]) -> list[GameProfile]:
        raise NotImplementedError


class AbstractProfileApiHandler(ABC):
    """材质管理 API Handler"""

    async def upload(self, *, accessToken: AuthorizationHeader, uuid: GameId,
                     textureType: Literal["skin", "cape"],
                     texture: UploadTexture) -> None:
        raise NotImplementedError

    async def remove(self, *, accessToken: AuthorizationHeader, uuid: GameId,
                     textureType: Literal["skin", "cape"]) -> None:
        raise NotImplementedError


class AbstractRootApiHandler(ABC):
    """元数据 API Handler"""

    async def home(self) -> MetaData:
        raise NotImplementedError

    def sign_key(self) -> RsaKey:
        raise NotImplementedError


# TODO：切记：改完后记得改yggdrasil.app.register

if __name__ == "__main__":
    from yggdrasil.test.pseudo.profiles import pseudo_game_profile, pseudo_user_profile

    test = UserApiResponse(accessToken="test1", clientToken="test2",
                           availableProfiles=[pseudo_game_profile()],
                           user=pseudo_user_profile())
    print(test)
    print(test.model_dump_json(exclude_unset=True))
    del test.user
    print(test)
    print(test.model_dump_json(exclude_unset=True))
