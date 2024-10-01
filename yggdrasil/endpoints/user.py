# coding=utf-8
from typing import Annotated

from fastapi import APIRouter, Depends

from yggdrasil.app import handlers
from yggdrasil.proto.interfaces.user import LoginRequest, RefreshRequest, UserApiResponse
from yggdrasil.exceptions import InvalidCredentials, InvalidToken

user_apis = APIRouter(prefix="/authserver")


@user_apis.post("/authenticate", response_model=UserApiResponse, response_model_exclude_none=True)
async def login(form: LoginRequest,
                result: Annotated[UserApiResponse, Depends(handlers.user.login)]
                ) -> UserApiResponse:
    """处理登录逻辑。TODO：在此预先处理速率限制"""
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


@user_apis.post("/refresh", response_model=UserApiResponse, response_model_exclude_none=True)
async def refresh(form: RefreshRequest,
                  result: Annotated[UserApiResponse, Depends(handlers.user.refresh)]
                  ) -> UserApiResponse:
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
    # 规范中未定义何时应相应 selectedProfile ，故不作处理。

    return result  # TODO：文档中写明返回值定义


@user_apis.post("/validate", status_code=204)
async def validate(result: Annotated[bool, Depends(handlers.user.validate)]) -> None:
    """处理验证令牌有效性逻辑"""
    if not result:
        raise InvalidToken


@user_apis.post("/invalidate", dependencies=[Depends(handlers.user.invalidate)], status_code=204)
async def invalidate() -> None:
    """处理吊销令牌逻辑"""
    # 由于不需要返回值，所以此处什么都不用做


@user_apis.post("/signout", status_code=204)
async def logout(result: Annotated[bool, Depends(handlers.user.logout)]) -> None:
    """处理登出逻辑。TODO：在此预先处理速率限制"""
    if not result:
        raise InvalidCredentials
