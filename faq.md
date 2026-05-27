

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

A: 可以。在 Inspector 中修改 `HeartbeatInterval`（默认 5 秒）和 `HeartbeatTimeout`（默认 60 秒），或在代码中直接赋值：

```csharp
client.HeartbeatInterval = 15f;
client.HeartbeatTimeout = 30f;
```

> **注意：** `HeartbeatInterval` 同时也是网络延迟（`CurrentPingMs`）的刷新间隔。更短的心跳间隔意味着更频繁的延迟更新，但也会增加网络开销。

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

### Q: 如何显示网络延迟？

A: 将 `PingDisplay` 组件挂载到任意场景 GameObject 上即可。它会自动查找 `LinkPlayClient` 并绑定 `OnPingUpdated` 事件，在屏幕右下角显示当前延迟。

延迟通过 ping/pong 机制测量：
- 客户端发送 `ping` 时记录 `Time.realtimeSinceStartup`
- 收到 `pong` 时计算差值（毫秒）→ `CurrentPingMs` → `OnPingUpdated`

### Q: SSL 证书错误怎么办？

A: SDK 默认启用了 `BypassSslCertificate = true`，会自动跳过 SSL 证书验证并启用 TLS 1.2。适用于自签名证书或内网穿透场景。

如需严格验证，将 `BypassSslCertificate` 设为 `false`。

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

### Q: LinkPlayClient.Instance 和直接引用有什么区别？

A: `Instance` 是一个静态单例，由第一个挂载了 `LinkPlayClient` 的 GameObject 在 `Start()` 中设置。后续 `LinkPlayClient` 实例会被自动销毁（`Destroy(gameObject)`）。

```csharp
// 任意位置获取客户端引用
var client = LinkPlayClient.Instance;
```


