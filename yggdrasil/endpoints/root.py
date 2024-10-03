# coding=utf-8
"""注册 Yggdrasil API 的元数据端点"""
from typing import Annotated, Any

from Crypto.PublicKey.RSA import RsaKey
from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder

from yggdrasil.endpoints import handlers
from yggdrasil.models.root import MetaData

root_endpoints = APIRouter()


@root_endpoints.get("/")
async def home(metadata: Annotated[MetaData, Depends(handlers.root.home)],
               sign_key: Annotated[RsaKey, Depends(handlers.root.sign_key)]) -> dict[str, Any]:
    """处理主页面源数据清单"""
    return jsonable_encoder(metadata) | {"signaturePublickey": sign_key.public_key().export_key().decode()}
