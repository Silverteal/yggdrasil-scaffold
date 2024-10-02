# coding=utf-8
from typing import Optional, override
from uuid import uuid4

from Crypto.PublicKey import RSA
from Crypto.PublicKey.RSA import RsaKey

from adofai import ClientToken, GameName, UserId
from adofai.profiles import GameProfile, UserProfile
from adofai.utils.profile import fake_token, offline_profile, parse_fake_token, prompt_profile
from adofai.utils.uuid import offline_uuid, uuid_to_str
from yggdrasil import fastapi_instance
from yggdrasil.handlers import register
from yggdrasil.handlers.proto import AbstractHandlerRoot, AbstractHandlerSession, AbstractHandlerUser
from yggdrasil.models.root import MetaData
from yggdrasil.models.session import JoinRequest
from yggdrasil.models.user import LoginRequest, LogoutRequest, RefreshRequest, UserEndpointsResponse, ValidationsRequest
from yggdrasil.utils.context import ClientIP


# @fastapi_instance.middleware("http")
# async def demo_middleware(request: Request, call_next):
#     response = await call_next(request)
#     return response


@register.root
class RootHandler(AbstractHandlerRoot):

    def __init__(self) -> None:
        self.key = RSA.generate(2048)

    @override
    async def home(self) -> MetaData:
        return MetaData(
            meta={
                "feature.non_email_login": True
            },
            skinDomains=[
                "."
            ]
        )

    @override
    async def sign_key(self) -> RsaKey:
        return self.key


@register.user
class UserHandler(AbstractHandlerUser):

    @override
    async def login(self, *, form: LoginRequest) -> UserEndpointsResponse | None:
        name = GameName(form.username)
        unique = offline_uuid(name)
        profile = GameProfile(id=unique, name=name)

        return UserEndpointsResponse(
            accessToken=fake_token(profile),
            clientToken=form.clientToken or ClientToken(uuid_to_str(uuid4())),
            availableProfiles=[prompt_profile("感谢您使用盗版验证v1.0"),
                               prompt_profile("登录请选择第三项，也就是您输入的用户名"),
                               profile,
                               prompt_profile(f"UUID：{unique}"),
                               prompt_profile(f"顺带一提，您的密码 {form.password} 超酷的")],
            selectedProfile=None,
            user=UserProfile(id=UserId(unique))
        )

    @override
    async def refresh(self, *, form: RefreshRequest) -> UserEndpointsResponse:
        return UserEndpointsResponse(
            accessToken=form.accessToken,
            clientToken=form.clientToken or ClientToken(uuid_to_str(uuid4())),
            selectedProfile=form.selectedProfile,
            user=UserProfile(id=UserId(parse_fake_token(form.accessToken).id))
        )

    @override
    async def validate(self, *, form: ValidationsRequest) -> bool:
        return True

    @override
    async def invalidate(self, *, form: ValidationsRequest) -> None:
        pass

    @override
    async def logout(self, *, form: LogoutRequest) -> bool:
        return True


@register.session
class SessionHandler(AbstractHandlerSession):

    @override
    async def join(self, *, form: JoinRequest, ip: ClientIP) -> bool:
        return True

    @override
    async def has_joined(self, *, username: str, serverId: str, ip: Optional[str] = None) -> GameProfile | None:
        return offline_profile(GameName(username))


fastapi_instance = fastapi_instance  # avoid gc
