---
layout: default
title: 常见问题
nav_order: 10
---

# 10. 常见问题

### Q: 断线后会自动重连吗？

A: 会。`AutoReconnect` 默认为 `true`。当 WebSocket 意外断开（非主动调用 `DisconnectAsync()`）且重连次数未达上限时，会自动尝试重连。可配置：

- `MaxReconnectAttempts` — 最大重连次数（-1 为无限）
- `ReconnectDelay` — 重连间隔（秒）

### Q: RPC 方法的参数有什么限制？

A: 参数必须是 JSON 可序列化的类型：
- ✅ `int`、`float`、`double`、`long`、`bool`、`string`
- ✅ `Dictionary<string, object>`
- ❌ `GameObject`、`Transform` 等 Unity 特有类型
- ❌ 自定义类（除非标记 `[Serializable]`）

### Q: RPC 方法可以是非 public 的吗？

A: 可以。`DispatchRPCMethod` 使用反射查找，支持 `public`、`private`、`protected` 方法。但建议标记为 `public` 以避免混淆。

### Q: 如何在 RPC 中传递复杂数据？

A: 使用 `Dictionary<string, object>`：

```csharp
// 发送
var data = new Dictionary<string, object>
{
    ["playerId"] = "abc123",
    ["position"] = new float[] { 1.0f, 2.0f, 3.0f },
    ["items"] = new int[] { 101, 202, 303 }
};
await client.InvokeRPCAsync("OnPlayerData", new object[] { data });

// 接收
[LinkPlayRPC]
public void OnPlayerData(Dictionary<string, object> data)
{
    string pid = data["playerId"].ToString();
    // ...
}
```

### Q: 心跳间隔可以修改吗？

A: 可以。在 Inspector 中修改 `HeartbeatInterval`（默认 30 秒）和 `HeartbeatTimeout`（默认 60 秒），或在代码中直接赋值：

```csharp
client.HeartbeatInterval = 15f;
client.HeartbeatTimeout = 30f;
```

### Q: 如何在 Unity 编辑器中测试联机？

A:
1. 启动服务端程序（DLMTP_LinkPlay_Socket_Server）
2. 在 Unity 中配置 `ServerUrl` 为 `ws://localhost:8080`（通过 `GameInfo` 设置）
3. 运行 Unity 场景，启动多个实例进行测试

### Q: `OnBroadcastReceived` 和具体事件（如 `OnRoomDetailInfoReceived`）有什么区别？

A:
- `OnBroadcastReceived` — **通用广播通道**，接收所有服务端推送上来的广播事件（玩家加入/离开、属性变更等）
- `OnRoomDetailInfoReceived` — **特定响应通道**，仅在调用 `GetCurrentRoomInfoAsync()` 后触发
- 建议：处理玩家加入/离开等广播用 `OnBroadcastReceived`；显示房间详情列表用 `OnRoomDetailInfoReceived`

### Q: ServerUrl 是如何确定的？

A: `ServerUrl` 是一个属性，根据 `GameInfo.Instance.gameLinkPlayServerType` 自动选择：

```csharp
public string ServerUrl => GameInfo.Instance.gameLinkPlayServerType switch
{
    GameInfo.URLType.Main      => GameInfo.Instance.gameLinkPlayUrlMain,
    GameInfo.URLType.Localhost => GameInfo.Instance.gameLinkPlayUrlLocalhost,
    _                          => GameInfo.Instance.gameLinkPlayUrlMain,
};
```

如果需要手动覆盖，直接赋值即可（不影响自动逻辑）。

---

[← 完整使用示例](examples.md) | [返回首页](index.md)
