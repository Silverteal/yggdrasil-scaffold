# coding=utf-8

from fastapi import APIRouter, Depends

from yggdrasil.api.preprocesser.user import *
from yggdrasil.proto.handlers.user import UserApiResponse

userapis = APIRouter(prefix="/authserver")


@userapis.post("/authenticate", response_model=UserApiResponse, response_model_exclude_none=True)
async def login(response_got: UserApiResponse = Depends(login)):
    return response_got


@userapis.post("/refresh", response_model=UserApiResponse, response_model_exclude_none=True)
async def refresh(response_got: UserApiResponse = Depends(refresh)):
    return response_got


@userapis.post("/validate")
async def validate(response_got=Depends(validate)):
    return response_got


@userapis.post("/invalidate")
async def invalidate(response_got=Depends(invalidate)):
    return response_got


@userapis.post("/signout")
async def logout(response_got=Depends(logout)):
    return response_got