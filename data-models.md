---
layout: default
title: 数据模型
nav_order: 5
---

# 5. 数据模型（LinkPlayModels）

## 5.1 网络协议模型

### ServerRequest

客户端发送到服务端的请求。

| 字段 | 类型 | 说明 |
|------|------|------|
| `type` | `string` | 请求类型（如 `"join_lobby"`） |
| `data` | `string` | JSON 对象字符串，承载请求参数 |
| `timestamp` | `long` | Unix 毫秒时间戳 |

**构造方法：** `ServerRequest(string typeStr, object dataObj = null)`

- `dataObj` 会被 `JsonUtility.ToJson` 序列化
- 无参数时 `data` 为 `"{}"`

**方法：**

| 方法 | 返回类型 | 说明 |
|------|----------|------|
| `ToJson()` | `string` | 将自身序列化为 JSON 字符串 |

---

### ServerResponse

服务端返回的响应。

| 字段 | 类型 | 说明 |
|------|------|------|
| `success` | `bool` | 是否成功 |
| `type` | `string` | 响应类型 |
| `data` | `string` | JSON 对象字符串，承载响应数据（可能为 null） |
| `error` | `ServerError` | 错误信息（success=false 时有效） |
| `timestamp` | `long` | Unix 毫秒时间戳 |

**方法：**

| 方法 | 返回类型 | 说明 |
|------|----------|------|
| `GetData<T>()` | `T` | 将 `data` 反序列化为指定类型；data 为空时返回 null |
| `FromJson(string json)` | `ServerResponse` | 从 JSON 字符串解析响应（静态方法） |

---

### ServerError

服务端错误信息。

| 字段 | 类型 | 说明 |
|------|------|------|
| `code` | `string` | 错误码（如 `"ROOM_NOT_FOUND"`） |
| `message` | `string` | 人类可读的错误描述 |

`ToString()` 返回格式：`[code] message`

---

### ServerBroadcast

服务端主动推送的广播消息。

| 字段 | 类型 | 说明 |
|------|------|------|
| `type` | `string` | 固定为 `"broadcast"` |
| `event` | `string` | 事件名（如 `"player_joined"`） |
| `roomId` | `string` | 房间标识 |
| `data` | `string` | 事件数据 JSON 字符串 |

**方法：**

| 方法 | 返回类型 | 说明 |
|------|----------|------|
| `FromJson(string json)` | `ServerBroadcast` | 从 JSON 字符串解析广播（静态方法） |

---

## 5.2 连接/大厅模型

### JoinLobbyData

`join_lobby` 请求参数。

| 字段 | 类型 | 说明 |
|------|------|------|
| `secret` | `string` | 服务器密钥，需与 `secret.json` 中的 `serverConnectSecret` 一致 |
| `playerName` | `string` | 玩家显示名称 |
| `playerId` | `string` | 玩家唯一 ID（UUID，由客户端 `Awake()` 时生成） |
| `playerDevicePlatform` | `string` | 运行平台，如 `"WindowsPlayer"`、`"Android"` |
| `playerDeviceModel` | `string` | 设备型号 |
| `playerDeviceOS` | `string` | 操作系统版本 |

---

### JoinLobbyResponse

`join_lobby` 成功后的响应数据。

| 字段 | 类型 | 说明 |
|------|------|------|
| `playerId` | `string` | 服务端确认的玩家 ID |

---

## 5.3 房间模型

### CreateRoomData

`create_room` 请求参数。

| 字段 | 类型 | 说明 |
|------|------|------|
| `roomName` | `string` | 房间名称 |
| `roomMaxPlayer` | `int` | 最大玩家数，自动 Clamp 在 2~50 之间 |
| `roomHasPassword` | `bool` | 是否有密码 |
| `roomPassword` | `string` | 密码（仅在 `roomHasPassword = true` 时传入） |
| `roomProperties` | `string` | JSON 对象字符串，自定义房间属性 |

**构造方法：** `CreateRoomData(string name, int maxPlayers, bool hasPassword, string password, Dictionary<string, object> properties)`

---

### RoomCreatedResponse

创建房间成功的返回数据。

| 字段 | 类型 | 说明 |
|------|------|------|
| `roomName` | `string` | 房间名称 |
| `roomMaxPlayer` | `int` | 最大玩家数 |
| `currentPlayerCount` | `int` | 当前玩家数 |
| `ownerPlayerId` | `string` | 房主玩家 ID |

---

### JoinRoomData

`join_room` 请求参数。

| 字段 | 类型 | 说明 |
|------|------|------|
| `roomName` | `string` | 要加入的房间名称 |
| `password` | `string` | 密码（无密码房间传空字符串） |

**构造方法：** `JoinRoomData(string name, string pwd)`

---

### RoomListItem

房间列表中的单个房间信息（公开发用）。

| 字段 | 类型 | 说明 |
|------|------|------|
| `roomName` | `string` | 房间名称 |
| `currentPlayerCount` | `int` | 当前玩家数 |
| `roomMaxPlayer` | `int` | 最大玩家数 |
| `roomHasPassword` | `bool` | 是否有密码 |
| `roomProperties` | `string` | 自定义属性（JSON 字符串） |

`ToString()` 返回格式：`Room[roomName] 3/10`（有密码时追加 🔒）。

---

### RoomListResponse

`get_room_list` 的响应数据。

| 字段 | 类型 | 说明 |
|------|------|------|
| `rooms` | `List<RoomListItem>` | 房间列表 |

---

### RoomDetailInfo

房间详细信息（包含玩家列表）（公开发用）。

| 字段 | 类型 | 说明 |
|------|------|------|
| `roomName` | `string` | 房间名称 |
| `roomMaxPlayer` | `int` | 最大玩家数 |
| `roomHasPassword` | `bool` | 是否有密码 |
| `roomProperties` | `string` | 自定义属性（JSON 字符串） |
| `ownerPlayerId` | `string` | 房主玩家 ID |
| `ownerPlayerName` | `string` | 房主玩家名称 |
| `players` | `List<PlayerDetailInfo>` | 房间内所有玩家信息列表 |

---

### SetRoomInfoData

`set_current_room_info` 请求参数（仅房主可调用）。

| 字段 | 类型 | 说明 |
|------|------|------|
| `roomProperties` | `string` | JSON 对象字符串 |

**构造方法：** `SetRoomInfoData(Dictionary<string, object> props)`

---

## 5.4 玩家模型

### PlayerDetailInfo

服务端返回的玩家信息（公开发用）。

| 字段 | 类型 | 说明 |
|------|------|------|
| `playerId` | `string` | 玩家唯一 ID |
| `playerName` | `string` | 玩家显示名称 |
| `playerDevicePlatform` | `string` | 运行平台 |
| `playerDeviceModel` | `string` | 设备型号 |
| `playerDeviceOS` | `string` | 操作系统版本 |
| `playerProperties` | `string` | 自定义玩家属性（JSON 字符串） |

`ToString()` 返回格式：`Player[playerName] ID:playerId`

---

### SetPlayerInfoData

`set_player_info` 请求参数。

| 字段 | 类型 | 说明 |
|------|------|------|
| `playerName` | `string` | 新玩家名称 |
| `playerProperties` | `string` | 自定义属性（JSON 字符串） |

**构造方法：** `SetPlayerInfoData(string newName, Dictionary<string, object> props)`

---

## 5.5 广播与游戏消息模型

### GameMessageData

`send_game_message` 请求参数。

| 字段 | 类型 | 说明 |
|------|------|------|
| `targetPlayers` | `List<string>` | 目标玩家 ID 列表；null 或空则广播给房间所有人 |
| `messageType` | `string` | 自定义消息类型（如 `"rpc"`） |
| `payload` | `string` | 自定义数据 JSON 字符串 |

**构造方法：** `GameMessageData(string msgType, object payloadObj, List<string> targets = null)`

---

### RPCPayload

RPC 调用数据（嵌入 `GameMessageData.payload` 中）。

| 字段 | 类型 | 说明 |
|------|------|------|
| `methodName` | `string` | 要调用的 RPC 方法名 |
| `parameters` | `string` | 参数数组的 JSON 字符串 |
| `targetType` | `int` | `RPCTargetType` 枚举值 |
| `senderId` | `string` | 发送者玩家 ID |
| `senderName` | `string` | 发送者玩家名称 |

**构造方法：** `RPCPayload(string method, object[] pars, RPCTargetType target, string senderIdVal, string senderNameVal)`

---

## 5.6 MiniJson 工具

简易 JSON 序列化/反序列化工具类，用于处理 `Dictionary<string, object>` 和数组。

**方法：**

| 方法 | 返回类型 | 说明 |
|------|----------|------|
| `Serialize(Dictionary<string, object> dict)` | `string` | 字典 → JSON 字符串 |
| `SerializeArray(object[] arr)` | `string` | 数组 → JSON 字符串 |
| `Deserialize(string json)` | `Dictionary<string, object>` | JSON 字符串 → 字典（仅支持扁平的 key:value） |
| `DeserializeArray(string json)` | `List<object>` | JSON 字符串 → 列表 |

**限制：** 反序列化仅支持**扁平的 key:value** 结构，不支持嵌套对象。

---

[← RPC 属性](rpc-attribute.md) | [下一章：核心客户端 →](client.md)
