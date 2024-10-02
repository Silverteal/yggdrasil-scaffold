# coding=utf-8
"""RSA 签名工具"""
__all__ = ["sign_property"]

from base64 import b64encode

from Crypto.Hash import SHA1
from Crypto.PublicKey.RSA import RsaKey
from Crypto.Signature import pkcs1_15


def sign_property(value: str, key: RsaKey) -> str:
    """以提供的值和 RSA 私钥对指定内容签名
    :param value: 待签名的值
    :param key: 用于签名的私钥
    :return: Base64 编码的签名结果
    """
    message = value.encode()
    h = SHA1.new(message)
    signature = b64encode(pkcs1_15.new(key).sign(h)).decode()
    return signature
