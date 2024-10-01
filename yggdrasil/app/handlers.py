# coding=utf-8
__all__ = []  # TODO注意：依赖项注册完成后，改变这里的引用并不会更新依赖项，使用隔壁的register。

from yggdrasil.proto.handlers import *

user: AbstractUserApiHandler = AbstractUserApiHandler()
session: AbstractSessionApiHandler = AbstractSessionApiHandler()
query: AbstractQueryApiHandler = AbstractQueryApiHandler()
profile: AbstractProfileApiHandler = AbstractProfileApiHandler()
root: AbstractRootApiHandler = AbstractRootApiHandler()
