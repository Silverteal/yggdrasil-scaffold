# coding=utf-8
"""用户 API 请求预处理"""
__all__ = ["login", "refresh", "validate", "invalidate", "logout"]

from typing import Any, Optional

from fastapi.responses import Response
from pydantic import BaseModel

from yggdrasil.proto.exceptions import InvalidCredentials, InvalidToken
from yggdrasil.api.apphandler.user import handler
from yggdrasil.proto.handlers.user import UserApiResponse
from yggdrasil.proto.profiles import GameProfile
from yggdrasil.proto.typealias import AccessToken, ClientToken, SerializedProfile, UserLoginName


class LoginRequestForm(BaseModel):
    username: UserLoginName
    password: str
    clientToken: Optional[ClientToken] = None
    requestUser: bool
    agent: Any = None


async def login(form: LoginRequestForm) -> UserApiResponse:
    """处理登录逻辑。TODO：在此预先处理速率限制"""
    result = await handler.login(username=form.username,
                                 password=form.password,
                                 clientToken=form.clientToken,
                                 requestUser=form.requestUser)
    # 验证和执行请求和返回与规范的一致性 TODO：使用 pydantic
    # 如果客户端没有请求用户，则将用户条目剥离
    if not form.requestUser:
        del result.user
    # 客户端请求了用户，但返回没有包含用户
    if form.requestUser and result.user is None:
        raise ValueError
    # 没有返回任何有效的 availableProfiles 值。即使没有有效值也应该返回空列表
    if result.availableProfiles is None:
        raise ValueError

    if result is not None:
        return result
    else:
        raise InvalidCredentials


class RefreshRequestForm(BaseModel):
    accessToken: AccessToken
    clientToken: Optional[ClientToken] = None
    requestUser: bool
    selectedProfile: Optional[SerializedProfile] = None


async def refresh(form: RefreshRequestForm) -> UserApiResponse:
    """处理刷新逻辑"""
    # 先反序列化 selectedProfile
    selected_profile = (
        GameProfile.deserialize(form.selectedProfile)
        if form.selectedProfile  # 防止 null 或空对象
        else None
    )

    result = await handler.refresh(accessToken=form.accessToken,
                                   clientToken=form.clientToken,
                                   requestUser=form.requestUser,
                                   selectedProfile=selected_profile)
    # 验证和执行请求和返回与规范的一致性 TODO：使用 pydantic
    # 如果客户端没有请求用户，则将用户条目剥离
    if not form.requestUser:
        del result.user
    # 客户端请求了用户，但返回没有包含用户
    if form.requestUser and result.user is None:
        raise ValueError
    # 响应中不应该包含 availableProfiles
    if result.availableProfiles is not None:
        raise ValueError
    # 规范中未定义何时应相应 selectedProfile ，故不作处理。

    return result  # TODO：文档中写明返回值定义


class ValidationsRequestForm(BaseModel):
    accessToken: AccessToken
    clientToken: Optional[ClientToken] = None


async def validate(form: ValidationsRequestForm) -> Response:
    """处理验证令牌有效性逻辑"""
    result = await handler.validate(accessToken=form.accessToken,
                                    clientToken=form.clientToken)
    if result:
        return Response(status_code=204)
    else:
        raise InvalidToken


async def invalidate(form: ValidationsRequestForm) -> Response:
    """处理吊销令牌逻辑"""
    await handler.invalidate(accessToken=form.accessToken)
    return Response(status_code=204)


class LogoutRequestForm(BaseModel):
    username: UserLoginName
    password: str


async def logout(form: LogoutRequestForm) -> Response:
    """处理登出逻辑。TODO：在此预先处理速率限制"""
    result = await handler.logout(username=form.username,
                                  password=form.password)
    if result:
        return Response(status_code=204)
    else:
        raise InvalidCredentials
