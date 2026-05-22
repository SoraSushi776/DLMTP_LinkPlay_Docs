---
layout: default
title: 消息处理器
nav_order: 7
---

# 7. 消息处理器（LinkPlayMessageHandler）

`LinkPlayMessageHandler` 是 `internal` 类，由 `LinkPlayClient` 内部使用，负责解析服务端返回的 JSON 消息并派发事件。

## 消息解析流程

```
原始消息
    │
    ├── 尝试解析为 ServerResponse（标准响应）
    │   ├── success=false → 触发 OnError
    │   └── success=true  → 根据 type 分派：
    │       ├── join_lobby        → OnConnected + OnJoinedLobby
    │       ├── leave_lobby       → OnLeftLobby
    │       ├── create_room       → OnRoomCreated
    │       ├── join_room         → OnRoomJoined
    │       ├── leave_room        → OnRoomLeft
    │       ├── get_room_list     → OnRoomListUpdated
    │       ├── get_current_room_info → OnRoomDetailInfoReceived
    │       ├── set_current_room_info → OnRoomInfoUpdated
    │       └── set_player_info   → OnPlayerInfoUpdated
    │
    ├── 尝试解析为 ServerBroadcast（广播）
    │   └── 根据 event 值分派：
    │       ├── player_joined             → OnBroadcastReceived("player_joined", data)
    │       ├── player_left               → OnBroadcastReceived("player_left", data)
    │       ├── room_properties_updated   → OnBroadcastReceived("room_properties_updated", data)
    │       ├── player_properties_updated → OnBroadcastReceived("player_properties_updated", data)
    │       └── 其他                      → OnBroadcastReceived(event, data)
    │
    ├── 识别为 pong → 更新心跳确认时间 + 计算 RTT 更新 CurrentPingMs + 触发 OnPingUpdated
    │
    └── 无法识别 → Debug.LogWarning
```

---

[← 核心客户端](client.md) | [下一章：协议格式 →](protocol.md)
