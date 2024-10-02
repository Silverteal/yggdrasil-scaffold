# coding=utf-8
"""UUID 工具包，主要包含玩家 UUID 相关的工具"""
__all__ = ["uuid_to_str", "offline_uuid", "pcl_offline_uuid"]

from hashlib import md5
from uuid import UUID

from adofai import GameId, GameName


def uuid_to_str(src: UUID | str, signed: bool = False) -> str:
    """
    从 UUID 对象或字符串生成小写的 UUID

    返回值与 str(self) 或 self.hex 相同

    >>> uuid_to_str("B50AD385829D3141A2167E7D7539BA7F", signed=True)
    'b50ad385-829d-3141-a216-7e7d7539ba7f'

    :param src: 原始的 UUID 对象或 UUID 格式文本
    :param signed: 布尔值，返回的文本是否有符号，默认为无符号
    :return: 小写的 UUID 文本
    """
    if isinstance(src, str):
        src = UUID(src)
    return str(src) if signed else src.hex


def offline_uuid(name: GameName) -> GameId:
    """
    从离线玩家的用户名生成原版规则的离线 UUID

    >>> offline_uuid(GameName("Notch"))
    UUID('b50ad385-829d-3141-a216-7e7d7539ba7f')
    >>> offline_uuid(GameName("Notch")).hex
    'b50ad385829d3141a2167e7d7539ba7f'

    :param name: 离线玩家的用户名
    :return: GameId 对象，表示专业服务器离线玩家的 UUID
    """
    return GameId(UUID(md5(("OfflinePlayer:" + name).encode()).hexdigest(), version=3))


def pcl_hash(src: str) -> int:
    """PCL2 使用的哈希模型
    :param src: 待计算哈希的字符串
    :return: 计算的哈希结果
    """
    num1 = 5381
    for i in src:
        num1 = (num1 << 5) ^ num1 ^ ord(i)
    ans = f"{num1 ^ 12218072394304324399:X}"
    return int.from_bytes(bytes.fromhex(ans[len(ans) - 16:]))


def pcl_offline_uuid(name: GameName) -> GameId:
    """PCL2 使用的离线 UUID 生成模型
    :param name: 离线玩家的用户名
    :return: GameId 对象，表示 PCL2 启动器离线房主玩家的 UUID
    """
    pad = lambda src, char, length: src[:length].rjust(length, char)
    full_uuid = pad(f"{len(name):X}", "0", 16) + pad(f"{pcl_hash(name):X}", "0", 16)
    full_uuid = full_uuid[0:12] + "3" + full_uuid[13:16] + "9" + full_uuid[17:32]
    return GameId(UUID(full_uuid))
