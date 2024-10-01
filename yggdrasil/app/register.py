# coding=utf-8
"""本模块是用于下级用户的的装饰器 TODO：目前只能通过测试用的覆盖接口来实现加载"""
from yggdrasil.app import handlers
from yggdrasil.endpoints import fastapi_instance
from yggdrasil.proto.handlers import *


def user(inst: AbstractUserApiHandler, /):
    """注册用户API处理程序"""
    fastapi_instance.dependency_overrides[handlers.user.login] = inst.login
    fastapi_instance.dependency_overrides[handlers.user.refresh] = inst.refresh
    fastapi_instance.dependency_overrides[handlers.user.validate] = inst.validate
    fastapi_instance.dependency_overrides[handlers.user.invalidate] = inst.invalidate
    fastapi_instance.dependency_overrides[handlers.user.logout] = inst.logout


def session(inst: AbstractSessionApiHandler, /):
    """注册会话API处理程序"""
    fastapi_instance.dependency_overrides[handlers.session.join] = inst.join
    fastapi_instance.dependency_overrides[handlers.session.has_joined] = inst.has_joined


def query(inst: AbstractQueryApiHandler, /):
    """注册查询API处理程序"""
    fastapi_instance.dependency_overrides[handlers.query.from_uuid] = inst.from_uuid
    fastapi_instance.dependency_overrides[handlers.query.from_name_batch] = inst.from_name_batch


def profile(inst: AbstractProfileApiHandler, /):
    """注册档案编辑API处理程序"""
    fastapi_instance.dependency_overrides[handlers.profile.upload] = inst.upload
    fastapi_instance.dependency_overrides[handlers.profile.remove] = inst.remove


def root(inst: AbstractRootApiHandler, /):
    """注册元数据API处理程序"""
    fastapi_instance.dependency_overrides[handlers.root.home] = inst.home
    fastapi_instance.dependency_overrides[handlers.root.sign_key] = inst.sign_key
