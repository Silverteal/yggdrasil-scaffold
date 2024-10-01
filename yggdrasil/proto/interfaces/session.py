# coding=utf-8
"""会话部分请求模型"""
__all__ = ["JoinRequest"]

from pydantic import BaseModel

from yggdrasil.proto.statictypes import AccessToken, GameId


class JoinRequest(BaseModel):
    """标准类型的会话请求表单"""
    accessToken: AccessToken
    selectedProfile: GameId  # 输入是 str，输出是 GameId
    serverId: str


if __name__ == '__main__':
    JoinRequest(
        accessToken='<PASSWORD>',
        selectedProfile='00000000-0000-0000-0000-000000000000',
        serverId='123',
    )
