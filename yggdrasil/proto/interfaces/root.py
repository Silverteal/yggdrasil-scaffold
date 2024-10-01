# coding=utf-8
__all__ = ["MetaData"]

from typing import Any

from pydantic import BaseModel

from yggdrasil.proto.statictypes import SkinDomainRule


# class ExtendableModel(BaseModel):
#     model_config = ConfigDict(extra='allow')
#
#     @model_serializer
#     def serialize(self, handler: SerializerFunctionWrapHandler):
#         """TODO：这邪门玩意真的能用吗"""
#         partial: dict[str, Any]
#         partial = handler(self)
#         returnable = {k: v for k, v in partial.items() if v is not None}
#         return returnable
#
#
# class MetaDataLinks(ExtendableModel):
#     homepage: str | None = None
#     register_: str | None = Field(default=None, alias="register")  # prevent covering internal attribute
#
#
#
# class MetaDataFields(ExtendableModel):
#     """服务器元数据“meta”字段的Schema"""
#     implementationName: str | None = "adofai-server"
#     implementationVersion: VersionNumber | None = FRAMEWORK_VERSION
#     serverName: str | None = None
#     links: MetaDataLinks | None = None


class MetaData(BaseModel):
    """除了签名公钥以外的服务器元数据"""
    meta: dict[str, Any]
    skinDomains: list[SkinDomainRule]
