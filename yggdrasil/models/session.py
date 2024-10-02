# coding=utf-8
"""会话端点的请求和返回模型"""
__all__ = ["JoinRequest"]

from pydantic import BaseModel

from adofai import AccessToken, GameId


class JoinRequest(BaseModel):
    """标准类型的会话请求表单
    :param accessToken: 访问令牌
    :param selectedProfile: 正在尝试加入服务器的玩家 UUID
    :param serverId: 玩家正在尝试加入的服务器标识符
    """
    accessToken: AccessToken
    selectedProfile: GameId  # 输入是 str，输出是 GameId
    serverId: str


if __name__ == '__main__':
    JoinRequest(
        accessToken='<PASSWORD>',
        selectedProfile='00000000-0000-0000-0000-000000000000',
        serverId='123',
    )
