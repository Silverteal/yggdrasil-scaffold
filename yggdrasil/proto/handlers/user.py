# coding=utf-8

from abc import ABC, abstractmethod
from typing import Optional

from pydantic import field_serializer

from yggdrasil.proto.handlers import AppResponse
from yggdrasil.proto.profiles import GameProfile, UserProfile
from yggdrasil.proto.typealias import AccessToken, ClientToken, SerializedProfile, UserLoginName


class UserApiResponse(AppResponse):
    accessToken: AccessToken
    clientToken: ClientToken
    availableProfiles: Optional[list[GameProfile]] = None
    selectedProfile: Optional[GameProfile] = None
    user: Optional[UserProfile] = None

    @field_serializer("availableProfiles", when_used="unless-none")
    def _export_ap(self, ap: Optional[list[GameProfile]]) -> list[SerializedProfile]:
        return [i.serialize("minimum") for i in ap]

    @field_serializer("selectedProfile", when_used="unless-none")
    def _export_sp(self, sp: Optional[GameProfile]) -> SerializedProfile:
        return sp.serialize("minimum")

    @field_serializer("user", when_used="unless-none")
    def _export_usr(self, usr: UserProfile) -> SerializedProfile:
        return usr.serialize()


class AbstractUserApiHandler(ABC):
    """用户 API Handler"""

    @abstractmethod
    async def login(self, username: UserLoginName, password: str, clientToken: ClientToken | None,
                    requestUser: bool) -> UserApiResponse | None:
        raise NotImplementedError

    @abstractmethod
    async def refresh(self, accessToken: AccessToken, clientToken: ClientToken | None,
                      requestUser: bool, selectedProfile: GameProfile | None) -> UserApiResponse:
        raise NotImplementedError

    @abstractmethod
    async def validate(self, accessToken: AccessToken, clientToken: ClientToken | None) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def invalidate(self, accessToken: AccessToken) -> None:
        raise NotImplementedError

    @abstractmethod
    async def logout(self, username: UserLoginName, password: str) -> bool:
        raise NotImplementedError


if __name__ == "__main__":
    from yggdrasil.pseudo.profiles import pseudo_game_profile, pseudo_user_profile

    test = UserApiResponse(accessToken="test1", clientToken="test2",
                           availableProfiles=[pseudo_game_profile()],
                           user=pseudo_user_profile())
    print(test)
    print(test.model_dump_json(exclude_unset=True))
    del test.user
    print(test)
    print(test.model_dump_json(exclude_unset=True))
