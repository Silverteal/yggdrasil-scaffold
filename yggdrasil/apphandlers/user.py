# coding=utf-8

__all__ = ["handler"]

from yggdrasil.pseudo.handlers.user import PseudoHandler

handler = PseudoHandler()  # TODO：临时的

if __name__ == "__main__":
    import asyncio

    instance = PseudoHandler()
    asyncio.run(instance.login(True))
