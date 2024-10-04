# coding=utf-8
from typing import override
from uuid import uuid4

from Crypto.PublicKey.RSA import RsaKey
from adofai import ClientToken, GameName, UserId
from adofai.models import FulfilledGameProfile, GameProfile, PartialGameProfile, UserProfile
from adofai.utils.profile import fake_token, parse_fake_token, prompt_game_profile
from adofai.utils.signing import dummy_key
from adofai.utils.uuid import offline_uuid, uuid_to_str
from yggdrasil_client import MojangProvider

from yggdrasil import fastapi_instance
from yggdrasil.handlers import register
from yggdrasil.handlers.proto import AbstractHandlerQuery, AbstractHandlerRoot, AbstractHandlerSession, \
    AbstractHandlerUser
from yggdrasil.models.root import MetaData
from yggdrasil.models.session import JoinRequest
from yggdrasil.models.user import LoginRequest, LogoutRequest, RefreshRequest, UserEndpointsResponse, ValidationsRequest
from yggdrasil.utils.context import ClientIP
from yggdrasil.utils.upstream import UpstreamWrapper


# @fastapi_instance.middleware("http")
# async def demo_middleware(request: Request, call_next):
#     response = await call_next(request)
#     return response


@register.root
class RootHandler(AbstractHandlerRoot):

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
        return dummy_key()


mojang_client = MojangProvider()
mojang = UpstreamWrapper(mojang_client)


@register.user
class UserHandler(AbstractHandlerUser):

    @override
    async def login(self, *, form: LoginRequest) -> UserEndpointsResponse | None:
        real_player_identifier = None
        uid = None
        name = GameName(form.username)
        profile = await mojang_client.query_by_name(name)
        if profile:
            real_player_identifier = "正版玩家"
            uid = profile.id
        else:
            real_player_identifier = "不存在玩家"
            uid = offline_uuid(name)

        profile = PartialGameProfile(GameProfile(id=uid, name=name))

        return UserEndpointsResponse(
            accessToken=fake_token(profile),
            clientToken=form.clientToken or ClientToken(uuid_to_str(uuid4())),
            availableProfiles=[prompt_game_profile("感谢您使用盗版验证v1.0"),
                               prompt_game_profile("登录请选择第三项，也就是您输入的用户名"),
                               profile,
                               prompt_game_profile(f"UUID：{uid}，{real_player_identifier}"),
                               prompt_game_profile(f"顺带一提，您的密码 {form.password} 超酷的")],
            selectedProfile=None,
            user=UserProfile(id=UserId(uid))
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
    async def has_joined(self, *, remote_result: mojang.has_joined) -> FulfilledGameProfile | None:
        return remote_result  # 此处通过调取依赖项直接将流量导向了 Mojang API


@register.query
class QueryHandler(AbstractHandlerQuery):

    @override
    async def query_by_names(self, *, remote_result: mojang.query_by_names) -> list[PartialGameProfile]:
        return remote_result  # 此处通过调取依赖项直接将流量导向了 Mojang API

    @override
    async def query_by_uuid(self, *, remote_result: mojang.query_by_uuid) -> FulfilledGameProfile | None:
        return remote_result  # 此处通过调取依赖项直接将流量导向了 Mojang API


fastapi_instance = fastapi_instance  # avoid gc
