# coding=utf-8
"""用户部分请求模型"""

__all__ = ["LoginRequest", "RefreshRequest", "ValidationsRequest", "LogoutRequest", "UserApiResponse"]

from typing import Annotated, Optional

from pydantic import BaseModel, field_serializer, field_validator

from yggdrasil.proto import LoosenBaseModel
from yggdrasil.proto.profiles import GameProfile, UserProfile
from yggdrasil.proto.statictypes import AccessToken, ClientToken, SerializedProfile, UserLoginName


class LoginRequest(BaseModel):
    username: UserLoginName
    password: str
    clientToken: Optional[ClientToken] = None
    requestUser: bool
    # agent: Any = None


class RefreshRequest(BaseModel):
    """标准类型的刷新请求表单，是Request Model的一部分"""
    accessToken: AccessToken
    clientToken: Optional[ClientToken] = None
    requestUser: bool
    selectedProfile: Annotated[
        Optional[SerializedProfile],
        GameProfile | None
    ] = None  # 一个Trick：实际handler读取到的是GameProfile | None。TODO：客户端代码可能因此无法通过类型检查。

    @field_validator("selectedProfile")
    @classmethod
    def ensure_profile(cls, v: Optional[SerializedProfile]) -> GameProfile | None:
        """将序列化的游戏档案反序列化"""
        return (GameProfile.deserialize(v)
                if v  # 防止 null 或空对象
                else None)


# class _RefreshRequest:
#     """作为依赖项供处理程序获取的刷新请求表单"""
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
    accessToken: AccessToken
    clientToken: Optional[ClientToken] = None


class LogoutRequest(BaseModel):
    username: UserLoginName
    password: str


class UserApiResponse(LoosenBaseModel):
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
