# coding=utf-8
from typing import Annotated, Any

from Crypto.PublicKey.RSA import RsaKey
from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder

from yggdrasil.app import handlers
from yggdrasil.proto.interfaces.root import MetaData

root_api = APIRouter()


@root_api.get("/")
async def home(metadata: Annotated[MetaData, Depends(handlers.root.home)],
               sign_key: Annotated[RsaKey, Depends(handlers.root.sign_key)]) -> dict[str, Any]:
    """处理主页面源数据清单"""
    return jsonable_encoder(metadata) | {"signaturePublickey": sign_key.public_key().export_key().decode()}


if __name__ == "__main__":
    from Crypto.PublicKey import RSA

    print(RSA.generate(2048).public_key().export_key().decode())
