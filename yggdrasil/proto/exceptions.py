# coding=utf-8

__all__ = ["YggdrasilException", "InvalidToken", "InvalidCredentials", "InvalidOwnership", "AlreadyBound"]

from collections.abc import Mapping
from typing import Optional

from fastapi import HTTPException
from fastapi.responses import JSONResponse


class YggdrasilException(HTTPException):
    """特定业务需要抛出的业务异常基类

    详见 https://github.com/yushijinhun/authlib-injector/wiki/Yggdrasil-%E6%9C%8D%E5%8A%A1%E7%AB%AF%E6%8A%80%E6%9C%AF%E8%A7%84%E8%8C%83#%E9%94%99%E8%AF%AF%E4%BF%A1%E6%81%AF%E6%A0%BC%E5%BC%8F
    """

    def __init__(
            self,
            status_code: int,
            error: str,
            errorMessage: str | None = None,
            cause: str | None = None,
    ) -> None:
        """
        :param status_code: 响应的状态码，规范的表格中对应 HTTP 状态码 列
        :param error: 响应的 ``error`` 字段，错误的简要描述（机器可读），规范的表格中对应 Error 列
        :param errorMessage: 响应的 ``errorMessage`` 字段，错误的详细信息（人类可读），规范的表格中对应 Error Message 列
        :param cause: 响应的 ``cause`` 字段，错误的原因（可选）。规范中定义为“一般不包含”
        """
        self.error = error
        self.errorMessage = errorMessage
        self.cause = cause
        super().__init__(status_code)


class ForbiddenOperationException(YggdrasilException):
    """适用于以下场景：
    令牌无效；
    密码错误，或短时间内多次登录失败而被暂时禁止登录；
    试图向一个令牌绑定不属于其对应用户的角色 *（非标准）*；
    试图使用一个错误的角色加入服务器。
    """

    def __init__(self, message: str, cause: Optional[str] = None) -> None:
        """
        详见 https://github.com/yushijinhun/authlib-injector/wiki/Yggdrasil-%E6%9C%8D%E5%8A%A1%E7%AB%AF%E6%8A%80%E6%9C%AF%E8%A7%84%E8%8C%83#%E9%94%99%E8%AF%AF%E4%BF%A1%E6%81%AF%E6%A0%BC%E5%BC%8F
        :param message: 错误的详细信息（人类可读）。规范的表格中对应 Error Message 列
        :param cause: 错误的原因（可选）
        """
        super().__init__(403, "ForbiddenOperationException", message, cause)


class IllegalArgumentException(YggdrasilException):
    """适用于以下场景：
    试图向一个已经绑定了角色的令牌指定其要绑定的角色。
    """

    def __init__(self,
                 message: str,  # 规范中此异常只对应此信息
                 cause: Optional[str] = None) -> None:
        """
        详见 https://github.com/yushijinhun/authlib-injector/wiki/Yggdrasil-%E6%9C%8D%E5%8A%A1%E7%AB%AF%E6%8A%80%E6%9C%AF%E8%A7%84%E8%8C%83#%E9%94%99%E8%AF%AF%E4%BF%A1%E6%81%AF%E6%A0%BC%E5%BC%8F
        :param message: 错误的详细信息（人类可读）。规范的表格中对应 Error Message 列
        :param cause: 错误的原因（可选）
        """
        super().__init__(400, "IllegalArgumentException", message, cause)


InvalidToken = ForbiddenOperationException("Invalid token.")
InvalidCredentials = ForbiddenOperationException("Invalid credentials. Invalid username or password.")
AlreadyBound = IllegalArgumentException("Access token already has a profile assigned.")
InvalidOwnership = ForbiddenOperationException("Trying to bind a game profile without appropriate ownership.")


def yggdrasil_error_response(status_code: int,
                             error: str,
                             errorMessage: str,
                             cause: Optional[str] = None,
                             headers: Optional[Mapping[str, str]] = None
                             ) -> JSONResponse:
    """
    根据给定参数生成异常。
    :param status_code: 响应的状态码
    :param error: 响应的 ``error`` 字段
    :param errorMessage: 响应的 ``errorMessage`` 字段
    :param cause: 响应的 ``cause`` 字段
    :param headers: 需要在响应中增加的头，预留备用
    :return:
    """
    structure = {"error": error, "errorMessage": errorMessage}
    if cause is not None:
        structure["cause"] = cause
    return JSONResponse(status_code=status_code, content=structure, headers=headers)
