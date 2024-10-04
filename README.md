# Yggdrasil Scaffold for Authlib-injector

基于 FastAPI 的 Yggdrasil 身份验证协议实现脚手架。

Yggdrasil 是 Minecraft 中身份验证服务的实现名称。

## 使用方式

### 安装

```shell
pip install yggdrasil-scaffold
```

详细的文档还没有写。但是这里有些资料：

### 可用资源

* `test`目录下有一些样例，模块内部有中文 docstring 和一些注释，暂时可供参考。

* `CONTRIBUTING.md` 中有本项目的术语表

* 关于 Yggdrasil API 的更多信息可参见
  [此文章](https://github.com/yushijinhun/authlib-injector/wiki/Yggdrasil-%E6%9C%8D%E5%8A%A1%E7%AB%AF%E6%8A%80%E6%9C%AF%E8%A7%84%E8%8C%83)

### 实现速查

如果你打算将本项目用于 Authlib-injector，那么下表列出了你需要实现的端点：

| 端点类型 | 客户端               | 服务端               |
|------|-------------------|-------------------|
| 用户   | /                 | /                 |
| 会话   | `join`            | `hasJoined`       |
| 查询   | `from_name_batch` | `from_name_batch` |
| 材质管理 | /                 | /                 |
| 元数据  | 全部                | 全部                |

注： Mojang 的身份认证库 Authlib 的一些早期版本包含对用户端点的调用，但最新版本中已移除。
我不确定用户端点是否在某些版本的游戏上有用，抑或是本就只在 Minecraft 启动器上可用。

游戏只会在”需要从玩家名获取 UUID“时才会访问查询端点。其它时候会从 `usercache.json` 或者类似的地方获取。

客户端进行多人游戏时，会访问元数据端点来验证材质签名。

如果你打算将本项目用于服务启动器，那么最好实现除`hasJoined`以外的全部端点，启动器很可能会用到它们。

## 警告

Yggdrasil Scaffold 并非被设计用于高并发或安全性要求高的用途，且未经严格测试。请谨慎在生产环境使用。

## 另请参阅

[ADOFAI](https://github.com/silverteal/adofai) 是一组数据模型和配套工具，旨在简化自定义实现 Authlib-injector 的规范
Yggdrasil 服务端、客户端及其配套程序的过程。