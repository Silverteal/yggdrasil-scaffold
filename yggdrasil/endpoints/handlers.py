# coding=utf-8
"""占位处理程序索引"""
__all__ = []  # TODO 注意：依赖项注册完成后，改变这里的引用并不会更新依赖项，请使用隔壁 register。

from yggdrasil.handlers.proto import *

user: AbstractHandlerUser = AbstractHandlerUser()
session: AbstractHandlerSession = AbstractHandlerSession()
query: AbstractHandlerQuery = AbstractHandlerQuery()
profile: AbstractHandlerProfile = AbstractHandlerProfile()
root: AbstractHandlerRoot = AbstractHandlerRoot()
