# coding=utf-8
from yggdrasil import fastapi_instance
from yggdrasil.handlers import register
from yggdrasil.test.pseudo.handlers import *

register.user(PseudoHandlerUser)
register.session(PseudoHandlerSession)
register.query(PseudoHandlerQuery)
register.profile(PseudoHandlerProfile)
register.root(PseudoHandlerRoot)

fastapi_instance = fastapi_instance
