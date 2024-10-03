# coding=utf-8
"""抽象处理程序的定义"""
__all__ = ["AbstractHandlerProfile", "AbstractHandlerQuery", "AbstractHandlerRoot",
           "AbstractHandlerSession", "AbstractHandlerUser"]

from abc import ABC
from typing import Literal, Optional

from Crypto.PublicKey.RSA import RsaKey

from adofai import GameId
from adofai.models import GameProfile
from yggdrasil.models.root import *
from yggdrasil.models.session import *
from yggdrasil.models.user import *
from yggdrasil.utils.context import AuthorizationHeader, ClientIP, UploadTexture


class AbstractHandlerUser(ABC):
    """用户端点处理程序抽象基类"""

    async def login(self, *, form: LoginRequest) -> UserEndpointsResponse | None:
        """使用密码进行身份验证，并分配一个新的令牌。

        若请求对象中未包含 clientToken，处理程序应该在响应对象中随机生成一个无符号 UUID 作为 clientToken。
        但需要注意 clientToken 可以为任何字符串，即请求对象中提供任何 clientToken 都是可以接受的，不一定要为无符号 UUID。

        对于令牌要绑定的玩家档案：
        若用户没有任何玩家档案，则为空；
        若用户仅有一个玩家档案，那么通常绑定到该玩家档案；
        若用户有多个玩家档案，通常为空，以便客户端进行选择。也就是说如果绑定的玩家档案为空，则需要客户端进行玩家档案选择。

        除使用邮箱登录外，处理程序还可以允许用户使用玩家名登录。
        要实现这一点，处理程序需要将元数据中的 feature.non_email_login 字段设置为 true。
        当用户使玩家名登录时，处理程序应自动将令牌绑定到相应玩家档案，即响应对象中的 selectedProfile 应为用户登录时所用的玩家档案。
        这种情况下，如果用户拥有多个玩家档案，那么他可以省去选择玩家档案的操作。
        考虑到某些程序不支持多玩家档案（例如 Geyser），还可以通过上述方法绕过玩家档案选择。

        安全警示：该端点可以被用于密码暴力破解，应受到速率限制。限制应针对用户，而不是客户端 IP。

        :param form: 请求的正文，包括登录凭据和可选的客户端令牌，详见类型文档
        :returns: 响应的正文，包含令牌、可用玩家档案、已选中玩家档案和用户信息等，详见类型文档；如果凭据无效或超出速率限制，返回 None。
        :raises InvalidCredentials: 凭据无效或超出速率限制时，也可以直接抛出异常
        """
        raise NotImplementedError

    async def refresh(self, *, form: RefreshRequest) -> UserEndpointsResponse:
        """吊销原令牌，并颁发一个新的令牌。

        当指定 clientToken 时，处理程序应检查 accessToken 和 clientToken 是否有效，否则只需要检查 accessToken。
        颁发的新令牌的 clientToken 应与原令牌的相同。

        如果请求中包含 selectedProfile，那么这就是一个选择玩家档案的操作。
        此操作要求原令牌所绑定的玩家档案为空，而新令牌则将绑定到 selectedProfile 所指定的玩家档案上。
        如果不包含 selectedProfile，那么新令牌所绑定的玩家档案和原令牌相同。

        刷新操作在令牌暂时失效时依然可以执行。若请求失败，原令牌依然有效。

        :param form: 请求的正文，包含原令牌、选择的玩家档案（可选）
        :returns: 响应的正文，包含新令牌，绑定的玩家档案等，详见类型文档
        :raises InvalidToken: 令牌无效
        :raises AlreadyBound: 试图向一个已经绑定了玩家档案的令牌指定其要绑定的玩家档案
        :raises InvalidOwnership: 试图向一个令牌绑定不属于其对应用户的玩家档案
        """
        raise NotImplementedError

    async def validate(self, *, form: ValidationsRequest) -> bool:
        """检验令牌是否有效。

        当指定 clientToken 时，处理程序应检查 accessToken 和 clientToken 是否有效，否则只需要检查 accessToken 。
        若令牌有效，处理程序应返回 True，无效则返回 False。此时也可以直接抛出令牌无效异常。

        :param form: 请求的正文，包含待验证的令牌，详见类型文档
        :returns: 一个布尔值，指示令牌是否有效
        :raises InvalidToken: 令牌无效时，也可以直接抛出异常
        """
        raise NotImplementedError

    async def invalidate(self, *, form: ValidationsRequest) -> None:
        """吊销给定令牌。

        处理程序只需要检查 accessToken，即无论 clientToken 为何值都不会造成影响。
        无论操作是否成功，都不需要返回值。

        :param form: 请求的正文，包含待吊销的令牌，详见类型文档
        """
        raise NotImplementedError

    async def logout(self, *, form: LogoutRequest) -> bool:
        """吊销用户的所有令牌。

        若成功完成吊销操作，处理程序应返回 True，凭据无效则返回 False，此时也可以直接抛出凭据无效异常。
        如果出现其他问题，则抛出对应业务异常。

        安全警示：该端点可以被用于密码暴力破解，应受到速率限制。限制应针对用户，而不是客户端 IP。

        :param form: 请求的正文，包括待吊销令牌用户的凭据，详见类型文档
        :returns: 一个布尔值，True 表示操作成功，False 表示凭据无效，其他情况下应该抛出对应异常
        :raises InvalidCredentials: 凭据无效时，也可以直接抛出异常
        """
        raise NotImplementedError


class AbstractHandlerSession(ABC):
    """用户端点处理程序抽象基类"""

    async def join(self, *, form: JoinRequest, ip: ClientIP) -> bool:
        """记录 Minecraft 服务端发送给客户端的 serverId，以备 Minecraft 服务端进行正版验证。

        仅当 accessToken 有效，且 selectedProfile 与令牌所绑定的玩家档案一致时，操作才成功。

        处理程序应记录以下信息：
        form.serverId
        form.accessToken
        ip（发送该请求的客户端 IP）

        实现时请注意：以上信息应记录在内存数据库中（如 Redis），且应该设置过期时间（如 30 秒）。
        鉴于 serverId 的随机性，可以将其作为主键。

        :param form: 请求的正文，包括服务器 ID，玩家令牌，玩家 ID 等信息，详见类型文档
        :param ip: 发送该请求的客户端 IP，默认为远程地址，可通过 FastAPI 中间件替换，或者通过 FastAPI 依赖项语法引入真实 IP
        :returns: 一个布尔值，True 表示操作成功，False 表示令牌无效或玩家 ID 不正确，其他情况下应该抛出对应异常
        :raises InvalidToken: 令牌无效或玩家 ID 不正确时，也可以直接抛出异常
        """
        raise NotImplementedError

    async def has_joined(self, *, username: str, serverId: str, ip: Optional[str] = None) -> GameProfile | None:
        """检查客户端会话的有效性，即数据库中是否存在该 serverId 的记录，且信息正确。

        username 需要与 serverId 所对应令牌所绑定的玩家名相同。

        返回加入玩家的玩家档案。如果没有相关记录或者玩家名不匹配，返回 None

        :param username: 正在加入服务器的玩家名
        :param serverId: 服务端发送给客户端的 serverId，标识该玩家正在加入的服务器
        :param ip: Minecraft 服务端获取到的客户端 IP，仅当 Minecraft 服务端 prevent-proxy-connections 选项开启时包含
        :returns: 响应的正文，即加入玩家的玩家档案，或返回 None 来表示没有可用的档案
        """
        raise NotImplementedError


class AbstractHandlerQuery(ABC):
    """查询端点处理程序抽象基类"""

    async def from_uuid(self, *, uuid: GameId) -> GameProfile | None:
        """查询指定玩家档案的完整信息（包含材质和属性）。

        :param uuid: 玩家 UUID（GameId，也就是 UUID 对象）
        :returns: 响应的正文，也就是玩家档案。如果没有查询到对应玩家，返回 None
        """
        raise NotImplementedError

    async def from_name_batch(self, *, names: list[str]) -> list[GameProfile]:
        """批量查询玩家名所对应的玩家档案。

        服务端查询各个玩家名所对应的玩家档案信息，并将其包含在响应中。不存在的玩家档案不需要包含。
        响应中玩家档案的先后次序无要求。

        安全提示：为防止 CC 攻击，需要为单次查询的玩家档案数目设置最大值，该值至少为 2。

        :param names: 正在查询的玩家名列表
        :returns: 玩家档案的列表，如果没有查询到任何玩家，返回空列表
        """
        raise NotImplementedError


class AbstractHandlerProfile(ABC):
    """材质管理端点处理程序抽象基类"""

    async def upload(self, *, accessToken: AuthorizationHeader, uuid: GameId,
                     textureType: Literal["skin", "cape"],
                     texture: UploadTexture) -> bool:
        """上传指定玩家档案的材质

        并非所有角色都可以上传皮肤和披风。要获取当前角色能够上传的材质类型，参见 Yggdrasil API Specification 中的相关论述。

        显然，应该先判断令牌和玩家 UUID 的有效性和匹配性，然后检查上传载荷，最后完成操作。

        传入的 texture 是一个定制的 fastapi.UploadFile 对象，表示正在上传的材质信息，查看 FastAPI 文档来了解如何处理文件。

        注意材质图像的 Content-Type 须为 image/png ，否则处理程序可以拒绝处理。
        有些客户端可能会设置 Content-Disposition 中的 filename 参数为材质图像的文件名，这可以用作材质的备注。

        对于皮肤，传入对象会有一个额外的 model 属性，填写了皮肤的材质模型，可以为 "slim"（细胳膊皮肤）或 "default"（普通皮肤）。
        需要特别注意的是，此处的 "default" 与原始请求中的 model 字段取值不同，
        原始请求中，如果皮肤是普通皮肤，model 字段会取值为空字符串。作出这个改变是为了保持框架内字段的一致性。

        :param accessToken: 访问令牌
        :param uuid: 目标玩家的 UUID
        :param textureType: 材质类型，可以为 "skin"（皮肤）或 "cape"（披风）
        :param texture: 上传的材质详情，详见 docstring 的正文部分。
        :returns: 一个布尔值，True 表示操作成功，False 表示令牌缺失或无效，其他情况下应该抛出对应异常
        """
        raise NotImplementedError

    async def remove(self, *, accessToken: AuthorizationHeader, uuid: GameId,
                     textureType: Literal["skin", "cape"]) -> bool:
        """清除材质，将对应材质恢复为默认。

        :param accessToken: 访问令牌
        :param uuid: 目标玩家的 UUID
        :param textureType: 材质类型，可以为 "skin"（皮肤）或 "cape"（披风）
        :returns: 一个布尔值，True 表示操作成功，False 表示令牌缺失或无效，其他情况下应该抛出对应异常
        """
        raise NotImplementedError


class AbstractHandlerRoot(ABC):
    """元数据端点处理程序抽象基类"""

    async def home(self) -> MetaData:
        """Authlib-injector 元数据端点

        理论上应该始终返回相同的元数据。

        元数据分为三部分，此处应通过返回 MetaData 对象提供其中的两部分：元数据和材质域名白名单。

        :returns: 代表元数据和材质域名白名单的 MetaData 对象，详见类型文档
        """
        raise NotImplementedError

    async def sign_key(self) -> RsaKey:
        """获取用于签名的 RSA Key 及元数据需要使用的公钥的端点

        理论上应该始终返回相同的 RSA Key

        :returns: 用于签名的 RSA Key
        """
        raise NotImplementedError

# TODO：切记：改完后记得改 register
