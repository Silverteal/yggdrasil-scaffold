# coding=utf-8

from abc import ABC, abstractmethod

from yggdrasil.proto.interfaces.user import *


class AbstractUserApiHandler(ABC):
    """用户 API Handler"""

    @abstractmethod
    async def login(self, *, form: LoginRequest) -> UserApiResponse | None:
        raise NotImplementedError

    @abstractmethod
    async def refresh(self, *, form: RefreshRequest) -> UserApiResponse:
        raise NotImplementedError

    @abstractmethod
    async def validate(self, *, form: ValidationsRequest) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def invalidate(self, *, form: ValidationsRequest) -> None:
        raise NotImplementedError

    @abstractmethod
    async def logout(self, *, form: LogoutRequest) -> bool:
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
