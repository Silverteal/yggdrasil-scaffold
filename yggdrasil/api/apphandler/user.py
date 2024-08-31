# coding=utf-8

__all__ = ["handler"]

from yggdrasil.pseudo.handlers.user import PseudoUserApiHandler

handler = PseudoUserApiHandler()  # TODO：临时的

if __name__ == "__main__":
    import asyncio

    instance = PseudoUserApiHandler()
    asyncio.run(instance.login("1", "1", None, True))
