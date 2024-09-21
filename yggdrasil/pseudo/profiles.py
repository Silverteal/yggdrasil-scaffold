# coding=utf-8
from random import choice, randint
from uuid import uuid4

from yggdrasil.proto.profiles import GameProfile, UserProfile
from yggdrasil.proto.textures import TextureProfile, TextureProperty
from yggdrasil.proto.typealias import GameName, TextureUrl, UserId
from yggdrasil.util import offline_uuid


def pseudo_user_profile() -> UserProfile:
    """用于测试用途的随机用户档案"""
    return UserProfile(
        id=UserId(uuid4()),
        properties={
            "preferredLanguage": choice(("en", "zh-CN", "en-CN", "en-GB", "en-US"))
        }
    )


def pseudo_game_profile() -> GameProfile:
    """用于测试用途的随机游戏档案"""
    return GameProfile(
        id=offline_uuid(a := GameName("player" + str(randint(1000, 9999)))),
        name=a,
        texture=pseudo_texture(),
        extra_properties={"uploadableTextures": choice(("skin", "cape", "skin,cape"))}
    )


def pseudo_texture() -> TextureProfile:
    """用于测试用途的随机材质档案"""
    return TextureProfile(SKIN=TextureProperty(TextureUrl("https://hostname/sha1"),
                                               {"model": choice(("default", "slim"))}),
                          CAPE=TextureProperty(TextureUrl("https://hostname/sha1")))


if __name__ == "__main__":
    print(pseudo_game_profile().serialize("unsigned"))