# coding=utf-8
"""注册 Yggdrasil API 的用户端点"""
from typing import Annotated

from fastapi import APIRouter, Depends

from yggdrasil.endpoints import handlers
from yggdrasil.exceptions import InvalidCredentials, InvalidToken
from yggdrasil.models.user import LoginRequest, RefreshRequest, UserEndpointsResponse

user_endpoints = APIRouter(prefix="/authserver")


@user_endpoints.post("/authenticate", response_model_exclude_none=True)
async def login(form: LoginRequest,
                result: Annotated[UserEndpointsResponse | None, Depends(handlers.user.login)]
                ) -> UserEndpointsResponse | None:
    """处理登录逻辑。TODO：在此预先处理速率限制"""
    # 验证和执行请求和返回与规范的一致性 TODO：使用 pydantic
    # 如果客户端没有请求用户，则将用户条目剥离
    if result is not None:
        if not form.requestUser:
            del result.user
        # 客户端请求了用户，但返回没有包含用户
        if form.requestUser and result.user is None:
            raise ValueError
        # 没有返回任何有效的 availableProfiles 值。即使没有有效值也应该返回空列表
        if result.availableProfiles is None:
            raise ValueError

        return result

    else:
        raise InvalidCredentials


@user_endpoints.post("/refresh", response_model_exclude_none=True)
async def refresh(form: RefreshRequest,
                  result: Annotated[UserEndpointsResponse, Depends(handlers.user.refresh)]
                  ) -> UserEndpointsResponse:
    """处理刷新逻辑"""
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
    # 响应的 selectedProfile 逻辑较为复杂，暂不作处理。

    return result


@user_endpoints.post("/validate", status_code=204)
async def validate(result: Annotated[bool, Depends(handlers.user.validate)]) -> None:
    """处理验证令牌有效性逻辑"""
    if not result:
        raise InvalidToken


@user_endpoints.post("/invalidate", dependencies=[Depends(handlers.user.invalidate)], status_code=204)
async def invalidate() -> None:
    """处理吊销令牌逻辑"""
    # 由于不需要返回值，所以此处什么都不用做


@user_endpoints.post("/signout", status_code=204)
async def logout(result: Annotated[bool, Depends(handlers.user.logout)]) -> None:
    """处理登出逻辑。TODO：在此预先处理速率限制"""
    if not result:
        raise InvalidCredentials
