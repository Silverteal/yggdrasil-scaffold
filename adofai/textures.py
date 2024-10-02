# coding=utf-8
"""材质信息数据类"""
import json
from base64 import b64decode, b64encode
from collections.abc import Mapping
from time import time_ns
from typing import Optional, Self, overload

from adofai import GameId, GameName, TextureUrl
from adofai.utils.uuid import uuid_to_str


class TextureProperty:
    """单个类型的材质属性，不含属性本身的名称"""

    def __init__(self, url: TextureUrl, metadata: Optional[Mapping[str, str]] = None) -> None:
        """创建一个属性。

        ``metadata`` 示例： ``{"model":"default"}``

        :param url: 一个 TextureURL ，详细规则见 https://github.com/yushijinhun/authlib-injector/wiki/Yggdrasil-%E6%9C%8D%E5%8A%A1%E7%AB%AF%E6%8A%80%E6%9C%AF%E8%A7%84%E8%8C%83#%E6%9D%90%E8%B4%A8-url-%E8%A7%84%E8%8C%83
        :param metadata: 一个映射类型，详见 https://github.com/yushijinhun/authlib-injector/wiki/Yggdrasil-%E6%9C%8D%E5%8A%A1%E7%AB%AF%E6%8A%80%E6%9C%AF%E8%A7%84%E8%8C%83#textures-%E6%9D%90%E8%B4%A8%E4%BF%A1%E6%81%AF%E5%B1%9E%E6%80%A7

        """
        self.url: TextureUrl
        self.metadata: dict[str, str] | None

        self.url = url
        self.metadata = dict(metadata) if metadata is not None else None


class TextureProfile:
    """
    材质档案 TODO：在文档中写明：元数据的字段名会自动转为小写，而序列化时会自动转为大写

    和直觉不同，此类只包含整个材质序列化格式中的 ``textures`` 字段，只在导出时组合其他字段。

    详见 https://github.com/yushijinhun/authlib-injector/wiki/Yggdrasil-%E6%9C%8D%E5%8A%A1%E7%AB%AF%E6%8A%80%E6%9C%AF%E8%A7%84%E8%8C%83#textures-%E6%9D%90%E8%B4%A8%E4%BF%A1%E6%81%AF%E5%B1%9E%E6%80%A7
    """

    @overload
    def __init__(self, **kwargs: TextureProperty) -> None:
        """通过 属性名-TextureProperty 的命名参数生成材质档案

        例：TextureProfile(skin=TextureProperty(TextureUrl("https://textures.host/texturehash"), {"model": "slim"}),
                          cape=TextureProperty(TextureUrl("https://textures.host/anothertexturehash")))
        :param kwargs: 关键字参数名称对应材质名称，参数值为 TextureProperty，对应该材质的内容。
        """

    @overload
    def __init__(self, textures: Mapping[str, Mapping[str, str]], /) -> None:
        """通过材质返回值格式的映射对象生成 TextureProfile

        例：TextureProfile(
            {
                "SKIN":
                    {
                        "url": TextureUrl("https://textures.host/texturehash"),
                        "metadata": {"model": "default"}
                    },
                "CAPE": {"url": TextureUrl("https://anothertextures.host/texturehash")}
            }
        )
        :param textures: 一个映射对象，详见以下结构中的``textures``： https://github.com/yushijinhun/authlib-injector/wiki/Yggdrasil-%E6%9C%8D%E5%8A%A1%E7%AB%AF%E6%8A%80%E6%9C%AF%E8%A7%84%E8%8C%83#textures-%E6%9D%90%E8%B4%A8%E4%BF%A1%E6%81%AF%E5%B1%9E%E6%80%A7
        """

    def __init__(self, *args, **kwargs):
        self.textures: dict[str, TextureProperty]

        if kwargs:
            self.textures = {k.lower(): v for k, v in kwargs.items()}
        else:
            textures = args[0]
            self.textures = {}
            for k, v in textures.items():
                self.textures[k.lower()] = TextureProperty(url=v["url"], metadata=v.get("metadata", None))

    @classmethod
    def deserialize(cls, src: str) -> Self:
        """从 base64 编码的字符串中恢复材质信息
        :param src: base64 序列化的材质字符串
        :return: 对应的材质对象
        """
        structure = json.loads(b64decode(src).decode())["textures"]
        return cls(structure)  # __init__ 用法 2

    def serialize(self, id: GameId, name: GameName, timestamp: Optional[int] = None) -> str:
        """以响应中使用的 base64 格式返回字符串
        :param id: 此材质所属游戏档案的 UUID
        :param name: 此材质所属游戏档案的用户名
        :param timestamp: 生成时间的毫秒级时间戳，不填则将以系统时间填充
        :return: base64 编码的材质信息响应字符串
        """
        structure = {
            "timestamp": timestamp or int(time_ns() / 1000000),
            "profileId": uuid_to_str(id),
            "profileName": name,
            "textures": {
                k.upper(): {
                    "url": v.url,
                    "metadata": v.metadata
                }
                for k, v in self.textures.items()
            }
        }
        for i in structure["textures"].values():
            if i["metadata"] is None:
                del i["metadata"]
        return b64encode(json.dumps(structure, ensure_ascii=False).encode()).decode()
