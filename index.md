

# DLMTP_LinkPlay SDK Wiki

> **命名空间：** `DLMTP_LinkPlay`
> **核心依赖：** `UnityEngine`、`websocket-sharp`
> **服务端对接：** [DLMTP_LinkPlay_Socket_Server](https://github.com/your-repo)
> **文档版本：** v2.0 | **最后更新：** 2026-05-17

---

## 1. 概述

**DLMTP_LinkPlay** 是一个基于 WebSocket 的 Unity 联机客户端 SDK，提供完整的房间管理和 RPC 远程调用功能。

### 功能特性

| 特性 | 说明 |
|------|------|
| ✅ WebSocket 连接管理 | 基于 `websocket-sharp` 的异步连接（SSL 绕过支持） |
| ✅ 大厅 + 房间系统 | 支持创建/加入/离开房间，密码保护 |
| ✅ RPC 远程调用 | 4 种广播目标：全部、房主、非房主、除自己外 |
| ✅ 事件回调系统 | 全异步操作均有对应事件通知 |
| ✅ 自动心跳保活 | 可配置间隔与超时时间 |
| ✅ 断线自动重连 | 可配置重连次数与间隔 |
| ✅ 自定义房间/玩家属性 | 支持 `Dictionary<string, object>` 灵活扩展 |
| ✅ 跨平台设备信息 | 自动收集平台、设备型号、OS 信息 |

### 架构概览

```
┌─────────────────────────────────────────────────────┐
│                     Unity 客户端                      │
│                                                      │
│  LinkPlayClient (MonoBehaviour)                      │
│  ├── 连接管理 (ConnectAsync / DisconnectAsync)       │
│  ├── 大厅管理 (LeaveLobbyAsync)                     │
│  ├── 房间管理 (CreateRoom / JoinRoom / LeaveRoom)   │
│  ├── 玩家信息 (UpdatePlayerInfoAsync)               │
│  ├── 游戏消息 (SendGameMessageAsync)                │
│  ├── RPC 系统 (InvokeRPCAsync)                      │
│  └── 心跳/重连 (自动)                               │
│         │                                            │
│         ▼ WebSocket                                  │
│  ┌──────────────────────────────────────┐            │
│  │  DLMTP_LinkPlay_Socket_Server (C#)  │            │
│  │  (独立控制台应用)                    │            │
│  └──────────────────────────────────────┘            │
└─────────────────────────────────────────────────────┘
```

---

## 📑 文档导航

### 快速入门
- [文件结构](getting-started.md) — 项目文件组织与快速入门

### API 参考
- [枚举与常量](enums.md) — 所有枚举、消息类型、错误码和广播事件
- [RPC 属性](rpc-attribute.md) — `[LinkPlayRPC]` 远程调用标记详解
- [数据模型](data-models.md) — 网络协议、房间、玩家等数据模型
- [核心客户端](client.md) — `LinkPlayClient` 完整 API 参考
- [消息处理器](message-handler.md) — 内部消息解析与事件派发

### 协议与示例
- [协议格式](protocol.md) — WebSocket 通信协议与数据流
- [完整使用示例](examples.md) — 连接、房间、RPC、位置同步示例
- [Game 组件](game-components.md) — LinkPlayContent 大厅入口 + PingDisplay 延迟显示

### 其他
- [常见问题](faq.md) — FAQ 与调试技巧

---

> **项目仓库：** https://github.com/your-repo/DLMTP_LinkPlay
> **问题反馈：** https://github.com/your-repo/DLMTP_LinkPlay/issues
