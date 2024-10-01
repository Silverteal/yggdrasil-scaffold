# coding=utf-8
"""单独定义所有类型别名，防止循环引入"""

__all__ = ["AccessToken", "ClientToken", "UserId", "UserLoginName", "GameId", "GameName", "TextureUrl",
           "VersionNumber", "ProfileProperties", "SerializedProfile"]

from collections.abc import Mapping
from typing import NewType
from uuid import UUID

AccessToken = NewType('AccessToken', str)
ClientToken = NewType('ClientToken', str)
UserId = NewType('UserId', UUID)
UserLoginName = NewType('UserLoginName', str)
GameId = NewType('GameId', UUID)
GameName = NewType('GameName', str)
TextureUrl = NewType('TextureUrl', str)
VersionNumber = NewType('VersionNumber', str)

type SkinDomainRule = str  # TODO：enhance or remove
type ProfileProperties = Mapping[str, str]
type SerializedProfile = dict[str, list[dict[str, str]] | str]
