---
layout: default
title: 核心客户端
nav_order: 6
---

# 6. 核心客户端（LinkPlayClient）

`LinkPlayClient` 是 SDK 的核心类，继承自 `MonoBehaviour`，底层使用 **websocket-sharp** 实现 WebSocket 通信。挂载到任意 GameObject 上即可使用。

**命名空间：** `DLMTP_LinkPlay.CoreSDK`

## 6.1 静态实例

| 成员 | 类型 | 说明 |
|------|------|------|
| `Instance` | `LinkPlayClient` | 全局单例引用。在 `Start()` 中自动设置，场景中只能存在一个实例 |

## 6.2 序列化字段（Inspector 可配置）

### 服务器配置

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `ServerUrl` | `string`（只读属性） | 根据 `GameInfo` 自动选择 | 根据 `GameInfo.Instance.gameLinkPlayServerType` 选择 Main / Localhost 地址 |
| `BypassSslCertificate` | `bool` | `true` | 跳过 SSL 证书验证，自签名证书/内网穿透场景必须开启 |
| `ServerSecret` | `string` | `"5eb9fca115d3..."` | 服务器密钥，需与 `secret.json` 中的 `serverConnectSecret` 一致 |
| `PlayerName` | `string` | `"Player"` | 玩家显示名称 |

### 心跳配置

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `HeartbeatInterval` | `float` | `5f` | 心跳发送间隔（秒），同时也是网络延迟刷新间隔 |
| `HeartbeatTimeout` | `float` | `60f` | 心跳超时时间（秒），超时未收到 pong 则判定断线 |

### 重连配置

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `AutoReconnect` | `bool` | `true` | 是否启用自动重连 |
| `MaxReconnectAttempts` | `int` | `5` | 最大重连次数（`-1` 为无限重连） |
| `ReconnectDelay` | `float` | `3f` | 重连间隔（秒） |

## 6.3 运行时属性

| 属性 | 类型 | 访问级别 | 说明 |
|------|------|----------|------|
| `IsConnected` | `bool` | 只读 | 是否已连接（内部状态为 `Connected`） |
| `IsInLobby` | `bool` | 只读 | 是否在大厅中 |
| `IsInRoom` | `bool` | 只读 | 是否在房间中 |
| `CurrentRoomName` | `string` | 只读 | 当前所在房间名称 |
| `PlayerId` | `string` | 只读 | 玩家的唯一标识（UUID，`Awake()` 时自动生成） |
| `CurrentState` | `ConnectionState` | 只读 | 当前连接状态 |
| `CurrentPingMs` | `int` | 只读 | 当前网络延迟（毫秒），`-1` 表示尚未测量 |

## 6.4 事件回调

所有事件均为 `Action` / `Action<T>` 委托类型，在主线程上触发。

### 连接事件

| 事件 | 签名 | 触发时机 |
|------|------|----------|
| `OnConnected` | `Action` | WebSocket 连接建立且 `join_lobby` 响应成功后 |
| `OnDisconnected` | `Action` | 连接断开（非主动断开时触发） |
| `OnError` | `Action<string>` | 发生任何错误时，参数为错误描述字符串 |

### 大厅事件

| 事件 | 签名 | 触发时机 |
|------|------|----------|
| `OnJoinedLobby` | `Action` | 成功加入大厅 |
| `OnLeftLobby` | `Action` | 离开大厅 |

### 房间事件

| 事件 | 签名 | 触发时机 |
|------|------|----------|
| `OnRoomCreated` | `Action<string>` | 房间创建成功，参数为房间名称 |
| `OnRoomJoined` | `Action<string>` | 成功加入房间，参数为房间名称 |
| `OnRoomLeft` | `Action<string>` | 离开房间，参数为之前所在的房间名称 |
| `OnRoomListUpdated` | `Action<List<RoomListItem>>` | 房间列表刷新，参数为 `RoomListItem` 列表 |
| `OnRoomInfoUpdated` | `Action` | 房间属性更新成功 |
| `OnRoomClosed` | `Action` | 房间被房主关闭 |
| `OnRoomDetailInfoReceived` | `Action<RoomDetailInfo>` | 收到当前房间的详细信息，参数包含玩家列表 |

### 玩家事件

| 事件 | 签名 | 触发时机 |
|------|------|----------|
| `OnPlayerInfoUpdated` | `Action` | 玩家信息更新成功 |

### 广播与 RPC 事件

| 事件 | 签名 | 触发时机 |
|------|------|----------|
| `OnBroadcastReceived` | `Action<string, object>` | 收到服务端推送的广播，参数为事件名和数据 |
| `OnRPCReceived` | `Action<string, string>` | 收到 RPC 调用，参数为方法名和参数 JSON |

### 网络延迟事件

| 事件 | 签名 | 触发时机 |
|------|------|----------|
| `OnPingUpdated` | `Action<int>` | 每次心跳收到 pong 后触发，参数为当前延迟（毫秒） |

**广播事件（`OnBroadcastReceived`）的常见 `event` 值：**

| 事件名 | 数据内容 |
|--------|----------|
| `"player_joined"` | 包含 `playerId`、`playerName` 等的字典 |
| `"player_left"` | 包含 `playerId`、`playerName` 等的字典 |
| `"room_properties_updated"` | 房间新属性 |
| `"player_properties_updated"` | 玩家新属性 |

## 6.5 公共方法

所有 `async` 方法均可 `await`，返回 `bool` 表示操作是否成功发送。

### 连接管理

#### `ConnectAsync()`

```csharp
public async Task<bool> ConnectAsync()
```

连接到 WebSocket 服务器并自动加入大厅。

- **底层：** 使用 `websocket-sharp` 的 `WebSocket.Connect()`（同步，在 `Task.Run` 中执行）
- **SSL：** 当 `BypassSslCertificate = true` 时自动跳过证书验证，并启用 TLS 1.2
- **防重入：** 若正在连接中（`_isConnecting = true`）则跳过重复调用
- **连接后流程：** WebSocket 握手成功 → `OnOpen` 标记 `_pendingJoinLobby` → 主线程 `Update()` 中发送 `join_lobby`
- **返回值：** `true` 表示连接请求已发出（等待 `OnConnected` / `OnJoinedLobby` 回调确认）
- **触发事件：** 成功 → `OnConnected` + `OnJoinedLobby`；失败 → `OnError`
- **注意：** 若已连接则直接返回 `true`

#### `DisconnectAsync()`

```csharp
public async Task<bool> DisconnectAsync()
```

主动断开连接。

- **说明：** 断开前会自动离开当前房间（如在房间中），然后发送 `leave_lobby` 请求
- **内部逻辑：** `LeaveRoomAsync()` → `SendRequest(LeaveLobby)` → `DisconnectInternal()`
- **触发事件：** 无（因为是主动断开，设置 `_intentionalDisconnect = true` 防止触发 `OnDisconnected`）

### 大厅功能

#### `LeaveLobbyAsync()`

```csharp
public async Task<bool> LeaveLobbyAsync()
```

离开大厅。

- **前提：** `IsInLobby` 必须为 `true`
- **说明：** 发送 `leave_lobby` 请求，服务端会清理玩家对象并断开连接
- **返回值：** `false` 表示不在大厅中

### 房间管理

#### `CreateRoomAsync()`

```csharp
public async Task<bool> CreateRoomAsync(
    string roomName,
    int maxPlayers = 10,
    bool hasPassword = false,
    string password = "",
    Dictionary<string, object> properties = null)
```

创建房间。

- **前提：** 已连接且在大厅中，且当前不在房间中
- **参数：**
  - `roomName` — 房间名称（必填）
  - `maxPlayers` — 最大玩家数，默认 10，Clamp 范围 2~50
  - `hasPassword` — 是否密码保护
  - `password` — 密码（`hasPassword=true` 时有效）
  - `properties` — 自定义属性字典（可选，使用 `MiniJson.Serialize` 序列化）
- **前置检查：** 未连接/不在大厅/已在房间中 → 触发 `OnError` 并返回 `false`
- **触发事件：** 成功 → `OnRoomCreated`；失败 → `OnError`

#### `JoinRoomAsync()`

```csharp
public async Task<bool> JoinRoomAsync(string roomName, string password = "")
```

加入房间。

- **前提：** 已连接且在大厅中，且当前不在房间中
- **参数：**
  - `roomName` — 目标房间名称
  - `password` — 房间密码（无密码房间传空字符串）
- **触发事件：** 成功 → `OnRoomJoined`；失败 → `OnError`

#### `LeaveRoomAsync()`

```csharp
public async Task<bool> LeaveRoomAsync()
```

离开当前房间。

- **前提：** 当前必须在房间中
- **副作用：** `IsInRoom = false`，`CurrentRoomName = ""`
- **触发事件：** 成功 → `OnRoomLeft`

#### `GetRoomListAsync()`

```csharp
public async Task<bool> GetRoomListAsync()
```

获取房间列表。

- **前提：** 已连接（不要求在大厅中也可以获取）
- **触发事件：** `OnRoomListUpdated`，参数为 `List<RoomListItem>`

#### `GetCurrentRoomInfoAsync()`

```csharp
public async Task<bool> GetCurrentRoomInfoAsync()
```

获取当前房间的详细信息（含玩家列表）。

- **前提：** 当前必须在房间中
- **触发事件：** `OnRoomDetailInfoReceived`，参数为 `RoomDetailInfo`

#### `UpdateRoomInfoAsync()`

```csharp
public async Task<bool> UpdateRoomInfoAsync(Dictionary<string, object> properties)
```

更新房间属性（**仅房主可用**）。

- **前提：** 当前必须在房间中
- **参数：** `properties` — 要更新的属性字典
- **触发事件：** `OnRoomInfoUpdated`

### 玩家信息

#### `UpdatePlayerInfoAsync()`

```csharp
public async Task<bool> UpdatePlayerInfoAsync(
    string newPlayerName = null,
    Dictionary<string, object> properties = null)
```

更新玩家信息。

- **前提：** 已连接
- **参数：**
  - `newPlayerName` — 新名称（`null` 表示不更改，内部使用当前 `PlayerName`）
  - `properties` — 自定义属性字典（可选）
- **触发事件：** `OnPlayerInfoUpdated`
- **副作用：** 如传入非空新名称，`PlayerName` 属性会同步更新

### 游戏消息 / RPC

#### `SendGameMessageAsync()`

```csharp
public async Task<bool> SendGameMessageAsync(
    string messageType,
    object payload,
    List<string> targetPlayers = null)
```

向房间内玩家发送自定义游戏消息。

- **前提：** 当前必须在房间中
- **参数：**
  - `messageType` — 自定义消息类型标识
  - `payload` — 消息数据（自动序列化为 JSON）
  - `targetPlayers` — 目标玩家 ID 列表；`null` 表示广播给所有人
- **底层：** 通过 `send_game_message` 请求发送
- **触发事件：** 目标玩家收到后触发 `OnBroadcastReceived`

#### `InvokeRPCAsync()`

```csharp
public async Task<bool> InvokeRPCAsync(
    string methodName,
    object[] parameters = null,
    RPCTargetType targetType = RPCTargetType.Others)
```

调用远程过程（RPC）。封装了 `SendGameMessageAsync`，内部以 `messageType = "rpc"` 发送。

- **前提：** 当前必须在房间中
- **参数：**
  - `methodName` — 目标 RPC 方法名（对应 `[LinkPlayRPC]` 的 `Name` 或方法名）
  - `parameters` — 参数数组（通过 `MiniJson.SerializeArray` 序列化）
  - `targetType` — 广播目标类型，默认 `Others`
- **默认值：** `targetType = RPCTargetType.Others`（除自己外的其他玩家）
- **内部：** 构造 `RPCPayload`（含 `methodName`, `parameters`, `targetType`, `senderId`, `senderName`），作为 `SendGameMessageAsync` 的 payload
- **触发事件：** 目标玩家收到后触发 `OnRPCReceived`，并自动派发到标记了 `[LinkPlayRPC]` 的方法

## 6.6 内部方法

以下方法为 `internal` 访问级别，通常不直接调用，但在扩展 SDK 时可能有参考价值。

| 方法 | 签名 | 说明 |
|------|------|------|
| `SendRequest` | `void SendRequest(string type, object dataObj = null)` | 发送请求到服务端（自动序列化为 `ServerRequest` JSON） |
| `DispatchRPCMethod` | `void DispatchRPCMethod(string methodName, string parametersJson)` | 遍历场景中所有 `MonoBehaviour`，查找 `[LinkPlayRPC]` 标记的方法并调用 |
| `InvokeOnMainThread` | `void InvokeOnMainThread(Action action)` | 将操作排入主线程执行队列（线程安全） |
| `SetConnectionState` | `void SetConnectionState(ConnectionState s)` | 设置连接状态 |
| `SetInLobby` | `void SetInLobby(bool v)` | 设置大厅状态 |
| `SetInRoom` | `void SetInRoom(bool v)` | 设置房间状态 |
| `SetRoomName` | `void SetRoomName(string name)` | 设置当前房间名称 |
| `UpdateLastHeartbeatAck` | `void UpdateLastHeartbeatAck()` | 更新最后一次心跳确认时间，并用 `Time.realtimeSinceStartup` 计算 RTT（毫秒），更新 `CurrentPingMs` 并触发 `OnPingUpdated` |

## 6.7 内部机制详解

### SSL 证书绕过

```csharp
// BypassSslCertificate = true 时：
_webSocket.SslConfiguration.EnabledSslProtocols = 
    System.Security.Authentication.SslProtocols.Tls12;
_webSocket.SslConfiguration.ServerCertificateValidationCallback = 
    (sender, certificate, chain, sslPolicyErrors) => true; // 总是返回 true
```

### 连接防重入

`ConnectAsync()` 使用 `_isConnecting` 标记防止并发调用。同时 `_webSocket.OnClose` 在 `_isConnecting = true` 时不触发重连，避免连接阶段的重连风暴。

### 主线程调度

所有 WebSocket 回调（`OnOpen`、`OnMessage`、`OnError`、`OnClose`）运行在 websocket-sharp 的内部线程上。`LinkPlayClient` 通过 `_mainThreadActions` 队列将所有事件回调排入 Unity 主线程执行：

```
WebSocket 线程 → InvokeOnMainThread() → _mainThreadActions 队列 → Update() 中出队执行
```

### join_lobby 延迟发送

由于 websocket-sharp 的 `Send()` 不能在 `OnOpen` 回调线程中调用，所以 `OnOpen` 只设置 `_pendingJoinLobby = true`，由 `Update()` 在主线程检查标记后调用 `SendJoinLobby()`。

---

[← 数据模型](data-models.md) | [下一章：消息处理器 →](message-handler.md)
