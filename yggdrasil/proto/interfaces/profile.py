# coding=utf-8
__all__ = ["AuthorizationHeader", "UploadTexture"]

from typing import Annotated, Literal, Optional

from fastapi import Depends, Form, Header, UploadFile

from yggdrasil.proto.typealias import AccessToken


async def get_token(authorization: Annotated[Optional[str], Header()] = None) -> AccessToken | None:
    """获取Authorization头，并去掉bearer头（如有）"""
    if not authorization:
        return None
    scheme, _, token = authorization.partition(" ")
    if scheme.lower() == "bearer":
        return AccessToken(token)
    else:
        return AccessToken(authorization)  # 非标准格式头，原样返回


AuthorizationHeader = Annotated[AccessToken | None, Depends(get_token)]


async def get_file(*, model: Annotated[Optional[Literal["slim", ""]], Form()] = None, file: UploadFile) -> UploadFile:
    """获取上传的文件，并向其中注入model字段"""
    file.model = model  # TODO：有没有不注入属性的解决方案？
    return file


UploadTexture = Annotated[UploadFile, Depends(get_file)]
