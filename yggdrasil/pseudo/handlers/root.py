# coding=utf-8
from typing import override

from yggdrasil.proto.handlers.root import AbstractRootApiHandler
from yggdrasil.proto.interfaces.root import MetaData


class PseudoHandler(AbstractRootApiHandler):
    @override
    async def home(self) -> MetaData:
        return MetaData(meta={}, skinDomains=[])
