# coding=utf-8
from typing import Any

from pydantic import BaseModel


class MetaData(BaseModel):
    """除了签名公钥以外的服务器元数据"""
    meta: dict[str, Any]
    skinDomains: list[str]

