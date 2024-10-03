术语表：

术语表中英文后第一个逗号前的是其中文参考翻译。

一般：

- app：应用，即此包的用户所实现并和本项目交互的的提供程序
- handler(s)：（应用）处理程序
- endpoint(s)：端点
- api：API，由于包含歧义，最好避免使用此名称；用于表示整个项目公开的一组或所有网络端点，抑或是单独的一个端点
- user：用户，即 Yggdrasil API 模型中的用户
    - user profile：用户档案
    - user id：用户 ID，即用户的唯一标识符（UUID）
    - user name：用户登录名
- game profile：玩家档案，即 Yggdrasil API 模型中的角色
    - game id：玩家 UUID，即玩家用于登录的 UUID
    - game name：玩家名，即玩家在游戏中展示的名称
- token：令牌
    - access token：访问令牌，以驼峰命名法出现时可保留英文原文
    - client token：客户端令牌，以驼峰命名法出现时可保留英文原文
- server id：服务器 ID，在 Minecraft 多人游戏中的一种标识服务器的随机文本，由游戏生成

作为端点类型：

- user：用户
    - login：登录
    - refresh：刷新
    - validate：验证
    - invalidate：吊销
    - logout：登出，即吊销全部
- session：会话
    - join：加入
    - has joined：验证，即正版验证
- query：查询
    - from name batch：批量查询玩家名
    - from uuid：查询玩家档案
- profile：材质管理
    - upload：上传
    - remove：移除
- root：元数据
    - home：主页面，即展示元数据、材质域名白名单和签名公钥的端点
    - sign key：签名密钥对

请尽量保持命名风格一致

添加新的 API 端点时：

1. 添加 endpoints 预处理程序
2. 添加 models 请求-响应模板
3. 添加 proto.handlers 处理程序 ABC
4. 添加 app.register 注册点
5. 编写 test.pseudo.handlers 测试用例
6. 编写样例请求