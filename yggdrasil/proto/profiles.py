# coding=utf-8
"""用户档案和游戏档案"""
from collections.abc import Iterable, Mapping
from typing import Any, Literal, Optional, Self, overload

from Crypto.PublicKey.RSA import RsaKey

from yggdrasil.proto.textures import TextureProfile
from yggdrasil.proto.typealias import GameId, GameName, ProfileProperties, SerializedProfile, UserId
from yggdrasil.util import offline_uuid, sign_property, uuid_to_str


class UserProfile:
    """Yggdrasil 用户的档案"""

    @overload
    def __init__(self, id: UserId | str) -> None:
        """创建没有属性的用户档案。
        :param id: Yggdrasil 用户档案的唯一标识符，应为一个无符号 UUID。接受一个 UUID 实例或者正确格式的 UUID 文本
        """

    @overload
    def __init__(self, id: UserId | str, properties: ProfileProperties) -> None:
        """创建有属性的用户档案。

        ``properties`` 示例： ``{"preferredLanguage":"zh_CN"}``

        :param id: Yggdrasil 用户档案的唯一标识符，应为一个无符号 UUID。接受一个 UUID 实例或者正确格式的 UUID 文本
        :param properties: 用户的属性。若干个键值对，键和值都必须为文本。
        """

    @overload
    def __init__(self, id: UserId | str, properties: Iterable[Mapping[str, str]]) -> None:
        """用 Yggdrasil 响应格式创建有属性的用户档案。

        Properties 示例： ``[{"name":"preferredLanguage","value":"zh_CN"}]``

        详见 https://github.com/yushijinhun/authlib-injector/wiki/Yggdrasil-%E6%9C%8D%E5%8A%A1%E7%AB%AF%E6%8A%80%E6%9C%AF%E8%A7%84%E8%8C%83#%E7%94%A8%E6%88%B7%E4%BF%A1%E6%81%AF%E7%9A%84%E5%BA%8F%E5%88%97%E5%8C%96
        :param id: Yggdrasil 用户档案的唯一标识符，应为一个无符号 UUID。接受一个 UUID 实例或者正确格式的 UUID 文本
        :param properties: 用户的属性。接受一个非映射的可迭代对象，其中每个项都是包含以`name`和`value`为键的两个键值对的映射，分别代表属性键和值。键和值都必须为文本。
        """

    def __init__(self, id, properties=None):
        self.id: UserId
        self.properties: ProfileProperties

        self.id = UserId(id)
        self.properties = {}

        if properties:
            if isinstance(properties, Mapping):
                self.properties = properties
            else:
                self.properties = {i["name"]: i["value"] for i in properties}

    def serialize(self) -> SerializedProfile:
        """导出响应格式的用户档案
        :return: 用户档案信息的字典格式，详见 https://github.com/yushijinhun/authlib-injector/wiki/Yggdrasil-%E6%9C%8D%E5%8A%A1%E7%AB%AF%E6%8A%80%E6%9C%AF%E8%A7%84%E8%8C%83#%E7%94%A8%E6%88%B7%E4%BF%A1%E6%81%AF%E7%9A%84%E5%BA%8F%E5%88%97%E5%8C%96
        """
        return {
            "id": uuid_to_str(self.id),
            "properties": [
                {
                    "name": k,
                    "value": v,
                }
                for k, v in self.properties.items()
            ]
        }


class GameProfile:
    """游戏内玩家档案"""

    @overload
    def __init__(self, id: GameId | str, name: GameName | str, *, texture: Optional[TextureProfile] = None) -> None:
        """创建除材质外没有附加属性的游戏角色档案。
        :param id: 游戏角色的 UUID，应为无符号的。接受一个 UUID 实例或者正确格式的 UUID 文本
        :param texture: 可选，玩家的材质，接受一个 TextureProfile 实例
        """

    @overload
    def __init__(self, id: GameId | str, name: GameName | str, *, texture: Optional[TextureProfile] = None,
                 extra_properties: ProfileProperties) -> None:
        """创建除材质外有属性的游戏角色档案。

        ``extra_properties`` 示例： {"uploadableTextures":"skin,cape"}

        :param id: 游戏角色的 UUID，应为无符号的。接受一个 UUID 实例或者正确格式的 UUID 文本
        :param texture: 可选，玩家的材质，接受一个 TextureProfile 实例
        :param extra_properties: 非标的，玩家角色“除材质外的属性”。若干个键值对，键和值都必须为文本。
        """

    @overload
    def __init__(self, id: GameId | str, name: GameName | str, *, texture: Optional[TextureProfile] = None,
                 extra_properties: Iterable[Mapping[str, str]]) -> None:
        """用 Yggdrasil 响应格式创建除材质外有属性的用户档案。

        ``extra_properties`` 示例： ``[{"name":"uploadableTextures","value":"skin,cape","signature":"iamsignature"}]``

        TODO：``signature`` 值目前不能进行自定义。框架将自行计算键值的签名。

        详见 https://github.com/yushijinhun/authlib-injector/wiki/Yggdrasil-%E6%9C%8D%E5%8A%A1%E7%AB%AF%E6%8A%80%E6%9C%AF%E8%A7%84%E8%8C%83#%E8%A7%92%E8%89%B2%E4%BF%A1%E6%81%AF%E7%9A%84%E5%BA%8F%E5%88%97%E5%8C%96
        :param id: 游戏角色的 UUID，应为无符号的。接受一个 UUID 实例或者正确格式的 UUID 文本
        :param texture: 可选，玩家的材质，接受一个 TextureProfile 实例
        :param extra_properties: 非标的，玩家角色“除材质外的属性”。接受一个非映射的可迭代对象，其中每个项都是包含以`name`和`value`为键的两个键值对的映射，分别代表属性键和值。都必须为文本。其它键会被忽略。
        """

    def __init__(self, *args, **kwargs):
        # 此处文档刻意缺省了一个实现细节：当 ``id`` 为假值（一般即 None）时，会根据 ``name`` 生成一个离线模式 UUID。
        # 有时候脑残写的东西将不得不写完
        self.id: GameId
        self.name: GameName
        self.texture: Optional[TextureProfile]
        self.extra_properties: ProfileProperties

        params: dict[str, Any] = {"id": None, "texture": None, "extra_properties": {}}

        for i in kwargs:
            if i in ("id", "name", "texture", "extra_properties"):
                params[i] = kwargs[i]
            else:
                raise TypeError(f"'{i}' is an invalid keyword argument for {__name__}")
        if (l := len(args)) > 2:
            raise TypeError(f"{__name__} takes at most 2 arguments ({l} given)")
        if l >= 2:
            params["name"] = args[1]
        if l >= 1:
            params["id"] = args[0]

        self.id = GameId(params["id"]) if params["id"] else offline_uuid(GameName(params["name"]))
        self.name = GameName(params["name"])
        self.texture = params["texture"]

        self.extra_properties = {}
        if isinstance(params["extra_properties"], Mapping):
            self.extra_properties = params["extra_properties"]
        else:
            self.extra_properties = {i["name"]: i["value"] for i in params["extra_properties"]}

    @classmethod
    def deserialize(cls, src: SerializedProfile) -> Self:
        """导入游戏角色档案为需要的格式。
        >>> from yggdrasil.pseudo.profiles import pseudo_game_profile
        >>> a = pseudo_game_profile().serialize("unsigned")
        >>> a
        >>> b = GameProfile.deserialize(a)
        >>> b.serialize("unsigned")

        """
        id = src["id"]
        name = src["name"]

        if "properties" not in src:
            return cls(id, name)

        texture = None
        for i, value in enumerate(src["properties"]):  # 这是一个列表
            if value["name"] == "textures":
                texture = TextureProfile.deserialize(value["value"])
                del src["properties"][i]
                break
        extra_properties = src["properties"]

        return cls(id, name, texture=texture, extra_properties=extra_properties)

    @overload
    def serialize(self, export_level: Literal["unsigned", "minimum"]) -> SerializedProfile:
        """不需要签名的序列化无须提供私钥"""

    @overload
    def serialize(self, export_level: Literal["full"], key: RsaKey) -> SerializedProfile:
        """需要签名的序列化必须提供私钥"""

    def serialize(self, export_level: Literal["full", "unsigned", "minimum"],
                  key: Optional[RsaKey] = None) -> SerializedProfile:
        """导出游戏角色档案为需要的格式。"""
        structure = {
            "id": uuid_to_str(self.id),
            "name": self.name,
        }

        if export_level == "minimum":
            return structure

        structure["properties"] = []

        if self.texture:
            structure["properties"] += [
                {
                    "name": "textures",
                    "value": self.texture.serialize(id=self.id, name=self.name),
                }
            ]

        structure["properties"] += [
            {
                "name": k,
                "value": v,
            }
            for k, v in self.extra_properties.items()
        ]

        if export_level == "unsigned":
            return structure

        for token in structure["properties"]:
            # TODO：迭代出的是否是引用？赋值是否有效？
            token["signature"] = sign_property(token["value"], key)

        return structure
