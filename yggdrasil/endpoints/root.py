# coding=utf-8
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from yggdrasil.apphandlers.root import handler
from yggdrasil.proto.interfaces.root import MetaData
from yggdrasil.runtime import config

rootapi = APIRouter()


@rootapi.get("/")
async def home(metadata: Annotated[MetaData, Depends(handler.home)]) -> JSONResponse:
    """处理主页面源数据清单"""
    result = jsonable_encoder(metadata)
    result["signaturePublickey"] = config.sign_key.public_key().export_key().decode()
    return JSONResponse(result)


if __name__ == "__main__":
    from Crypto.PublicKey import RSA

    print(RSA.generate(2048).public_key().export_key().decode())
