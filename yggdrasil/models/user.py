# coding=utf-8
"""用户端点的请求和返回模型"""
__all__ = ["LoginRequest", "RefreshRequest", "ValidationsRequest", "LogoutRequest", "UserEndpointsResponse"]

from typing import Annotated, Optional

from pydantic import BaseModel, field_serializer, field_validator

from adofai import AccessToken, ClientToken, GameProfile, SerializedProfile, UserLoginName, UserProfile
from yggdrasil.models import LoosenBaseModel


class LoginRequest(BaseModel):
    """登录端点请求模型
    :param username: 用户登录名，典型地，这个值可以是邮箱或者该用户下的一个玩家名
    :param password: 密码
    :param clientToken: （可选）启动器为此次登录生成的客户端令牌"""
    username: UserLoginName
    password: str
    clientToken: Optional[ClientToken] = None
    requestUser: bool
    # agent: Any = None


class RefreshRequest(BaseModel):
    """刷新端点请求模型
    :param accessToken: 访问令牌
    :param clientToken: （可选）客户端令牌
    :param requestUser: 布尔值，是否返回用户。对于处理程序而言，这决定了响应不包含 UserProfile 时是否会报错
    :param selectedProfile: （可选）如有，则对处理程序而言是 GameProfile 实例，即客户端要求新令牌绑定的玩家档案"""
    accessToken: AccessToken
    clientToken: Optional[ClientToken] = None
    requestUser: bool
    selectedProfile: Annotated[
        Optional[SerializedProfile],
        GameProfile | None
    ] = None  # 一个Trick：实际处理程序读取到的是GameProfile | None。TODO：处理程序代码可能因此无法通过类型检查。

    @field_validator("selectedProfile")
    @classmethod
    def ensure_profile(cls, v: Optional[SerializedProfile]) -> GameProfile | None:
        """将序列化的游戏档案反序列化"""
        return (GameProfile.deserialize(v)
                if v  # 防止 null 或空对象
                else None)


# class _RefreshRequest:
#     """作为依赖项供处理程序获取的刷新端点请求模型"""
#
#     def __init__(self, model: _RefreshRequestModel):
#         self.accessToken: AccessToken
#         self.clientToken: Optional[ClientToken]
#         self.requestUser: bool
#         self.selectedProfile: Optional[GameProfile]
#
#         self.accessToken = model.accessToken
#         self.clientToken = model.clientToken
#         self.requestUser = model.requestUser
#         self.selectedProfile = (
#             GameProfile.deserialize(model.selectedProfile)
#             if model.selectedProfile  # 防止 None 或空对象
#             else None
#         )
#
#
# RefreshRequest = Annotated[_RefreshRequest, Depends()]


class ValidationsRequest(BaseModel):
    """验证/吊销端点共用请求模型
    :param accessToken: 访问令牌
    :param clientToken: （可选）客户端令牌
    """
    accessToken: AccessToken
    clientToken: Optional[ClientToken] = None


class LogoutRequest(BaseModel):
    """登出/全部吊销端点请求模型
    :param username: 用户登录名
    :param password: 密码
    """
    username: UserLoginName
    password: str


class UserEndpointsResponse(LoosenBaseModel):
    """部分用户端点共用的返回模型
    登录和刷新接口共用的返回模型，两端点所使用的字段略有不同

    关于 selectedProfile 的值：
    登录时：
    1. 当前请求的用户登录名是该用户的一个有效的玩家名——设为此玩家名对应的档案
    2. 当前用户只有一个玩家档案——设为此玩家档案
    其他情况下，无需设定 selectedProfile
    刷新时：
    1. 请求中包含 selectedProfile 且请求使用的 accessToken 尚未绑定到任何玩家档案——设为请求中 selectedProfile 对应的玩家档案
    2. 请求中不含 selectedProfile 且请求使用的 accessToken 已经绑定到一个玩家档案——设为此令牌已绑定的玩家档案
    其他情况下，无需设定 selectedProfile

    :param accessToken: 访问令牌
    :param clientToken: 客户端令牌，必填，如果客户端没有给，就生成一个 UUID 然后储存并返回
    :param availableProfiles: （仅登录时需要）已登录用户的可用玩家档案列表
    :param selectedProfile: （可选）当前访问令牌已绑定的玩家档案。见上
    :param user: （可选）当前上下文的用户，requestUser 为 True 时需要包含。
    """
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
