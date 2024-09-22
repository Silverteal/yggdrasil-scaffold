# coding=utf-8
from abc import ABC, abstractmethod

from yggdrasil.proto.interfaces.root import MetaData


class AbstractRootApiHandler(ABC):
    """元数据 API Handler"""

    @abstractmethod
    async def home(self) -> MetaData:
        raise NotImplementedError
