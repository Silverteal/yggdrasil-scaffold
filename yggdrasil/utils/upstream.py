# coding=utf-8
"""
[CAUTION] 尚在测试中
此模块中的组件只能在安装了可选依赖组``upstream``时才能使用
依赖安装方式：
``pip install yggdrasil-scaffold[upstream]``

用例详见 test.tryupstream
"""
import warnings
from typing import Annotated, Literal

from adofai.models import FulfilledGameProfile, PartialGameProfile
from fastapi import Depends
from yggdrasil_client import AbstractProvider, MojangProvider


class UpstreamWrapper:
    """Yggdrasil Client 的 dependable 包装器，目前，除了可以不写 Annotated 外，和直接使用 YC 当依赖项差别不大"""

    def __init__(self, provider: AbstractProvider) -> None:
        warnings.warn("尚未开发完成，使用风险自负", FutureWarning)
        self.provider = provider

        self.has_joined = Annotated[FulfilledGameProfile | Literal[False], Depends(provider.has_joined)]
        self.query_by_names = Annotated[list[PartialGameProfile], Depends(provider.query_by_names)]
        self.query_by_uuid = Annotated[FulfilledGameProfile | None, Depends(provider.query_by_uuid)]


if __name__ == "__main__":
    UpstreamWrapper(MojangProvider())
