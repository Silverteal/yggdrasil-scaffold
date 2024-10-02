# coding=utf-8
"""档案CRUD相关工具"""
__all__ = ["offline_profile", "prompt_profile", "fake_token", "parse_fake_token"]

import json
from base64 import b64decode, b64encode
from uuid import uuid4

from adofai.profiles import GameProfile
from adofai import AccessToken, GameId, GameName
from adofai.utils.uuid import offline_uuid


def offline_profile(name: GameName) -> GameProfile:
    """根据玩家名快速生成玩家档案"""
    return GameProfile(id=offline_uuid(name), name=name)


def prompt_profile(info: str):
    """生成纯文字的，用于文本提示的伪玩家档案，应用场景不多"""
    return GameProfile(GameId(uuid4()), GameName(info))


def fake_token(profile: GameProfile) -> AccessToken:
    """在安全性不敏感的场景，将游戏档案直接序列化为 AccessToken"""
    return AccessToken(b64encode(json.dumps(profile.serialize("unsigned")).encode()).decode())


def parse_fake_token(token: AccessToken) -> GameProfile:
    """在安全性不敏感的场景，解析游戏档案直接序列化的 AccessToken"""
    return GameProfile.deserialize(json.loads(b64decode(token)))
