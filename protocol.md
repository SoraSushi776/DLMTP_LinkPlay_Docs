---
layout: default
title: 协议格式
nav_order: 8
---

# 8. 协议格式说明

## JSON 协议示例

```json
// 客户端→服务端：加入大厅
{
    "type": "join_lobby",
    "data": "{\"secret\":\"your_secret\",\"playerName\":\"Player1\",\"playerId\":\"abc123...\",\"playerDevicePlatform\":\"WindowsPlayer\",\"playerDeviceModel\":\"...\",\"playerDeviceOS\":\"...\"}",
    "timestamp": 1712345678901
}

// 服务端→客户端：响应
{
    "success": true,
    "type": "join_lobby",
    "data": "{\"playerId\":\"abc123...\"}",
    "error": null,
    "timestamp": 1712345678902
}

// 服务端→客户端：广播
{
    "type": "broadcast",
    "event": "player_joined",
    "roomId": "Room_1234",
    "data": "{\"playerId\":\"def456...\",\"playerName\":\"Player2\"}"
}

// 心跳（纯文本，非 JSON）
客户端 → 服务端: "ping"
服务端 → 客户端: "pong"
```

## 数据流时序

```
客户端                             服务端
  │                                 │
  ├── ping ──────────────────────►  │
  │                                 │
  │◄── pong ───────────────────────┤
  │                                 │
  ├── {"type":"join_lobby",...}──►  │
  │                                 │
  │◄── {"success":true,"type":      │
  │      "join_lobby",...}──────────┤
  │                                 │
  ├── {"type":"create_room",...}──► │
  │                                 │
  │◄── {"success":true,"type":      │
  │      "create_room",...}─────────┤
  │                                 │
  │◄── {"type":"broadcast",         │
  │      "event":"player_joined",   │
  │      ...}───────────────────────┤ (其他玩家加入时)
  │                                 │
  ├── {"type":"send_game_message",  │
  │      "data":{"messageType":     │
  │      "rpc",...},...}───────────►│
  │                                 │
  │◄── (服务端转发 RPC 给目标玩家)─┤
  │                                 │
```

---

[← 消息处理器](message-handler.md) | [下一章：完整使用示例 →](examples.md)
