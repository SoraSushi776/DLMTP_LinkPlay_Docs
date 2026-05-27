

# 3. 枚举与常量（LinkPlayEnums）

## 3.1 ConnectionState

WebSocket 连接状态枚举。

| 值 | 说明 |
|----|------|
| `Disconnected` | 未连接 |
| `Connecting` | 正在连接 |
| `Connected` | 已连接 |
| `Reconnecting` | 正在重连 |
| `Disconnecting` | 正在断开 |

## 3.2 RPCTargetType

RPC 远程调用的广播目标类型。

| 值 | 说明 | 典型场景 |
|----|------|----------|
| `AllPlayersInRoom` | 房间内**所有玩家**（包括自己） | 游戏开始、倒计时、全局事件 |
| `RoomOwner` | **仅房主** | 报告状态、请求权限 |
| `NonOwnerPlayers` | **所有非房主玩家** | 游戏状态同步、通知 |
| `Others` | **除自己外的其他玩家** | 玩家动作同步（移动、攻击等） |

> **注意：** `ServerMessageType`、`ServerErrorCode`、`BroadcastEvent` 均为 `internal` 类，仅供 SDK 内部使用。此处列出仅供参考和调试。

## 3.3 ServerMessageType

与服务端约定的消息类型字符串常量。

| 常量名 | 值 | 方向 | 说明 |
|--------|-----|------|------|
| `Ping` | `"ping"` | 客户端→服务端 | 心跳请求 |
| `Pong` | `"pong"` | 服务端→客户端 | 心跳响应 |
| `JoinLobby` | `"join_lobby"` | 客户端→服务端 | 加入大厅 |
| `LeaveLobby` | `"leave_lobby"` | 客户端→服务端 | 离开大厅 |
| `CreateRoom` | `"create_room"` | 客户端→服务端 | 创建房间 |
| `JoinRoom` | `"join_room"` | 客户端→服务端 | 加入房间 |
| `LeaveRoom` | `"leave_room"` | 客户端→服务端 | 离开房间 |
| `GetRoomList` | `"get_room_list"` | 客户端→服务端 | 获取房间列表 |
| `GetCurrentRoomInfo` | `"get_current_room_info"` | 客户端→服务端 | 获取当前房间详情 |
| `SetCurrentRoomInfo` | `"set_current_room_info"` | 客户端→服务端 | 更新房间属性（房主） |
| `SetPlayerInfo` | `"set_player_info"` | 客户端→服务端 | 更新玩家信息 |
| `SendGameMessage` | `"send_game_message"` | 客户端→服务端 | 发送自定义游戏消息 |
| `Broadcast` | `"broadcast"` | 服务端→客户端 | 服务端主动广播推送 |

## 3.4 ServerErrorCode

服务端可能返回的错误码常量。

| 常量名 | 值 | 说明 |
|--------|-----|------|
| `InvalidRequest` | `"INVALID_REQUEST"` | 无效请求格式 |
| `AuthFailed` | `"AUTH_FAILED"` | 认证失败（密钥错误） |
| `RoomNotFound` | `"ROOM_NOT_FOUND"` | 房间不存在 |
| `RoomFull` | `"ROOM_FULL"` | 房间已满 |
| `WrongPassword` | `"WRONG_PASSWORD"` | 房间密码错误 |
| `AlreadyInRoom` | `"ALREADY_IN_ROOM"` | 已在房间中 |
| `NotInRoom` | `"NOT_IN_ROOM"` | 不在房间中 |
| `NotRoomOwner` | `"NOT_ROOM_OWNER"` | 不是房主（无操作权限） |
| `PlayerNotFound` | `"PLAYER_NOT_FOUND"` | 玩家不存在 |
| `ServerError` | `"SERVER_ERROR"` | 服务端内部错误 |

## 3.5 BroadcastEvent

服务端主动推送的广播事件类型常量。

| 常量名 | 值 | 说明 |
|--------|-----|------|
| `PlayerJoined` | `"player_joined"` | 有玩家加入房间 |
| `PlayerLeft` | `"player_left"` | 有玩家离开房间 |
| `RoomPropertiesUpdated` | `"room_properties_updated"` | 房间属性变更 |
| `PlayerPropertiesUpdated` | `"player_properties_updated"` | 玩家属性变更 |
| `GameStart` | `"game_start"` | 游戏开始（预留） |
| `GameEnd` | `"game_end"` | 游戏结束（预留） |


