

# 2. 文件结构

```
Assets/Scripts/DLMTP_LinkPlay/
├── CoreSDK/
│   ├── LinkPlayClient.cs          # 核心客户端类（MonoBehaviour，基于 websocket-sharp）
│   ├── LinkPlayEnums.cs           # 枚举与常量定义（ConnectionState, RPCTargetType, ServerMessageType 等）
│   ├── LinkPlayMessageHandler.cs  # 消息处理器（内部，解析服务端 JSON 并派发事件）
│   ├── LinkPlayModels.cs          # 数据模型 + MiniJson 工具 + 内部请求/响应类
│   └── LinkPlayRPCAttribute.cs    # [LinkPlayRPC] 方法标记特性
├── Game/
│   ├── LinkPlayContent.cs         # 大厅入口按钮脚本（一键加入联机大厅）
│   └── PingDisplay.cs             # 网络延迟 UI 显示组件（OnGUI）
└── README.md                      # 快速入门文档
```

## 目录说明

### CoreSDK/
SDK 核心层，提供 WebSocket 连接、房间管理、RPC 远程调用等所有联机功能。

| 文件 | 职责 |
|------|------|
| `LinkPlayClient.cs` | 核心 MonoBehaviour，挂载到场景 GameObject 上使用。提供连接/房间/RPC 等全部公共 API |
| `LinkPlayEnums.cs` | 定义 `ConnectionState`、`RPCTargetType` 枚举和 `ServerMessageType`、`ServerErrorCode`、`BroadcastEvent` 常量类 |
| `LinkPlayMessageHandler.cs` | 消息派发器，解析服务端 JSON 响应并按 type 分派到对应事件 |
| `LinkPlayModels.cs` | 数据类集合，包含 `RoomListItem`、`RoomDetailInfo`、`PlayerDetailInfo` 等公开模型，以及 `ServerRequest`/`ServerResponse` 等内部协议类。还包含 `MiniJson` 工具类 |
| `LinkPlayRPCAttribute.cs` | `[LinkPlayRPC]` 特性定义，用于标记可远程调用的方法 |

### Game/
游戏层组件，提供开箱即用的 UI 功能。

| 文件 | 职责 |
|------|------|
| `LinkPlayContent.cs` | 大厅入口按钮脚本。点击后调用 `ConnectAsync()` 连接服务器，成功后切换页面并自动获取房间列表 |
| `PingDisplay.cs` | 网络延迟显示组件。通过 `OnPingUpdated` 事件获取延迟，在屏幕右下角用 `OnGUI` 渲染，按延迟级别着色 |


