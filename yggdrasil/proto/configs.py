# coding=utf-8
from typing import Optional

from Crypto.PublicKey.RSA import RsaKey

from yggdrasil.proto import LoosenBaseModel


class YggdrasilConfig(LoosenBaseModel):
    sign_key: RsaKey
    ali: Optional[str] = None  # API 地址指示，如 ``/api/yggdrasil/``