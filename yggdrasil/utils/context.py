# coding=utf-8
"""用于提取请求特定上下文的工具，得益于 FastAPI 高效而灵活的依赖注入系统，这些工具的使用方法十分简单。"""
__all__ = ["ClientIP", "AuthorizationHeader", "UploadTexture"]

from typing import Annotated, Literal, Optional

from fastapi import Depends, Form, Header, Request, UploadFile

from adofai import AccessToken


async def get_client_ip(req: Request) -> str:
    """获取客户端连接IP
    :usage: 将 ClientIP 设为参数的类型提示
    """
    return req.client.host


ClientIP = Annotated[str, Depends(get_client_ip)]


async def get_token(authorization: Annotated[Optional[str], Header()] = None) -> AccessToken | None:
    """获取Authorization头，并去掉bearer头（如有）
    :usage: 将 AuthorizationHeader 设为参数的类型提示
    """
    if not authorization:
        return None
    scheme, _, token = authorization.partition(" ")
    if scheme.lower() == "bearer":
        return AccessToken(token)
    else:
        return AccessToken(authorization)  # 非标准格式头，原样返回


AuthorizationHeader = Annotated[AccessToken | None, Depends(get_token)]


async def get_texture_file(*,
                           model: Annotated[Optional[Literal["slim", ""]], Form()] = None,
                           file: UploadFile) -> UploadFile:
    """获取上传的材质文件，并向其中注入model字段"""
    if hasattr(file, "model"):
        match model:
            case "":
                file.model = "default"  # TODO：有没有不注入属性的解决方案？
            case _:
                file.model = model
    return file


UploadTexture = Annotated[UploadFile, Depends(get_texture_file)]
