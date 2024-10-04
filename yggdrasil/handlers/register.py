# coding=utf-8
"""本模块是用于下级用户的的装饰器 TODO：目前只能通过测试用的覆盖接口来实现加载"""
from typing import Type

from yggdrasil.endpoints import fastapi_instance, handlers
from yggdrasil.handlers.proto import *


def user(cls: Type[AbstractHandlerUser], /):
    """注册用户API处理程序"""
    inst = cls()
    fastapi_instance.dependency_overrides[handlers.user.login] = inst.login
    fastapi_instance.dependency_overrides[handlers.user.refresh] = inst.refresh
    fastapi_instance.dependency_overrides[handlers.user.validate] = inst.validate
    fastapi_instance.dependency_overrides[handlers.user.invalidate] = inst.invalidate
    fastapi_instance.dependency_overrides[handlers.user.logout] = inst.logout


def session(cls: Type[AbstractHandlerSession], /):
    """注册会话API处理程序"""
    inst = cls()
    fastapi_instance.dependency_overrides[handlers.session.join] = inst.join
    fastapi_instance.dependency_overrides[handlers.session.has_joined] = inst.has_joined


def query(cls: Type[AbstractHandlerQuery], /):
    """注册查询API处理程序"""
    inst = cls()
    fastapi_instance.dependency_overrides[handlers.query.query_by_uuid] = inst.query_by_uuid
    fastapi_instance.dependency_overrides[handlers.query.query_by_names] = inst.query_by_names


def profile(cls: Type[AbstractHandlerProfile], /):
    """注册档案编辑API处理程序"""
    inst = cls()
    fastapi_instance.dependency_overrides[handlers.profile.upload] = inst.upload
    fastapi_instance.dependency_overrides[handlers.profile.remove] = inst.remove


def root(cls: Type[AbstractHandlerRoot], /):
    """注册元数据API处理程序"""
    inst = cls()
    fastapi_instance.dependency_overrides[handlers.root.home] = inst.home
    fastapi_instance.dependency_overrides[handlers.root.sign_key] = inst.sign_key
