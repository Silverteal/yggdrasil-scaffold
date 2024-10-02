# coding=utf-8
"""元数据端点的请求和返回模型"""
__all__ = ["MetaData"]

from typing import Any

from pydantic import BaseModel


class MetaData(BaseModel):
    """除了签名公钥以外的服务器元数据
    :param meta: 元数据字典，例：
    {
        "implementationName": "yggdrasil-mock-server",
        "implementationVersion": "0.0.1",
        "serverName": "yushijinhun's Example Authentication Server",
        "links": {
            "homepage": "https://skin.example.com/",
            "register": "https://skin.example.com/register"
        },
        "feature.non_email_login": true
    }
    :param skinDomains: 域名规则白名单，支持完整匹配和子域名泛匹配，例：
    [
        "example.com",
        ".example.com"
    ]
    """
    meta: dict[str, Any]
    skinDomains: list[str]

# class ExtendableModel(BaseModel):
#     model_config = ConfigDict(extra='allow')
#
#     @model_serializer
#     def serialize(self, handler: SerializerFunctionWrapHandler):
#         """这邪门玩意真的能用吗"""
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
