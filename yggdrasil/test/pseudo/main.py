# coding=utf-8
from yggdrasil import fastapi_instance
from yggdrasil.app import register
from yggdrasil.test.pseudo.handlers import *

register.user(PseudoUserApiHandler())
register.session(PseudoSessionApiHandler())
register.query(PseudoQueryApiHandler())
register.profile(PseudoProfileApiHandler())
register.root(PseudoRootApiHandler())

fastapi_instance = fastapi_instance
