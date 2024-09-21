# coding=utf-8
"""会话部分请求模型"""
__all__ = ["JoinRequest"]

from typing import Annotated
from uuid import UUID

from pydantic import BaseModel

from yggdrasil.proto.typealias import AccessToken, GameId


class JoinRequest(BaseModel):
    """标准类型的会话请求表单，是Request Model的一部分"""
    accessToken: AccessToken
    selectedProfile: GameId  # 输入是 str，输出是 GameId
    serverId: str

    # @field_validator("selectedProfile")
    # @classmethod
    # def just_try(cls, v: str) -> GameId:
    #     """验证selectedProfile是否是有效的UUID，并转换为GameId"""
    #     return GameId(UUID(v))


# class _SessionRequest:
#     """作为依赖项供处理程序获取的会话请求表单"""
#
#     def __init__(self, model: _SessionRequestModel):
#         self.accessToken: AccessToken
#         self.selectedProfile: GameId  # GameId 类型是 UUID
#         self.serverId: str
#
#         self.accessToken = model.accessToken
#         self.selectedProfile = GameId(UUID(model.selectedProfile))
#         self.serverId = model.serverId
#
#
# JoinRequest = Annotated[_SessionRequest, Depends()]

if __name__ == '__main__':
    JoinRequest(
        accessToken='<PASSWORD>',
        selectedProfile='00000000-0000-0000-0000-000000000000',
        serverId='123',
    )
