

# 9. 完整使用示例

## 9.1 基础连接与大厅

```csharp
using UnityEngine;
using DLMTP_LinkPlay;
using DLMTP_LinkPlay.CoreSDK;

public class ConnectionManager : MonoBehaviour
{
    public LinkPlayClient client;

    private void Start()
    {
        // 动态添加组件
        if (client == null)
            client = gameObject.AddComponent<LinkPlayClient>();

        // 配置
        client.ServerSecret = "your_server_secret";
        client.PlayerName = "玩家" + Random.Range(1000, 9999);

        // 绑定事件
        client.OnConnected += () => Debug.Log("✅ 已连接");
        client.OnDisconnected += () => Debug.Log("❌ 已断开");
        client.OnError += (err) => Debug.LogError($"⚠️ {err}");
        client.OnJoinedLobby += () => Debug.Log("🎮 已加入大厅");
        client.OnLeftLobby += () => Debug.Log("👋 已离开大厅");

        // 连接
        _ = Connect();
    }

    private async System.Threading.Tasks.Task Connect()
    {
        bool ok = await client.ConnectAsync();
        if (!ok) Debug.LogError("连接失败");
    }

    private void OnDestroy()
    {
        if (client != null)
            _ = client.DisconnectAsync();
    }
}
```

## 9.2 房间管理

```csharp
using UnityEngine;
using DLMTP_LinkPlay;
using DLMTP_LinkPlay.CoreSDK;
using System.Collections.Generic;

public class RoomManager : MonoBehaviour
{
    public LinkPlayClient client;

    private void Start()
    {
        client.OnRoomCreated += (name) =>
        {
            Debug.Log($"🏠 房间创建成功: {name}");
        };

        client.OnRoomJoined += (name) =>
        {
            Debug.Log($"🚪 已加入房间: {name}");
            // 加入后获取房间详情
            _ = client.GetCurrentRoomInfoAsync();
        };

        client.OnRoomLeft += (name) =>
        {
            Debug.Log($"🚶 离开房间: {name}");
        };

        client.OnRoomListUpdated += (rooms) =>
        {
            Debug.Log($"📋 房间列表: {rooms.Count} 个房间");
            foreach (var room in rooms)
            {
                Debug.Log($"  {room.roomName} ({room.currentPlayerCount}/{room.roomMaxPlayer})" +
                          (room.roomHasPassword ? " 🔒" : ""));
            }
        };

        client.OnRoomDetailInfoReceived += (info) =>
        {
            Debug.Log($"📄 房间详情: {info.roomName}");
            Debug.Log($"   房主: {info.ownerPlayerName} ({info.ownerPlayerId})");
            Debug.Log($"   玩家 ({info.players.Count}):");
            foreach (var p in info.players)
                Debug.Log($"     - {p.playerName} ({p.playerId})");
        };
    }

    // 创建公开房间
    public async void CreatePublicRoom(string name)
    {
        await client.CreateRoomAsync(name, maxPlayers: 10);
    }

    // 创建加密房间
    public async void CreatePrivateRoom(string name, string password)
    {
        await client.CreateRoomAsync(name, maxPlayers: 4,
            hasPassword: true, password: password);
    }

    // 创建带自定义属性的房间
    public async void CreateCustomRoom(string name)
    {
        var props = new Dictionary<string, object>
        {
            ["gameMode"] = "BattleRoyale",
            ["mapName"] = "Desert",
            ["roundTime"] = 300
        };
        await client.CreateRoomAsync(name, maxPlayers: 20, properties: props);
    }

    // 加入房间
    public async void JoinRoom(string name, string password = "")
    {
        await client.JoinRoomAsync(name, password);
    }

    // 获取房间列表
    public async void RefreshRoomList()
    {
        await client.GetRoomListAsync();
    }

    // 更新房间属性（仅房主）
    public async void SetRoomProperty(string key, object value)
    {
        await client.UpdateRoomInfoAsync(
            new Dictionary<string, object> { { key, value } });
    }
}
```

## 9.3 RPC 远程调用

```csharp
using UnityEngine;
using DLMTP_LinkPlay;
using DLMTP_LinkPlay.CoreSDK;

public class GameRPC : MonoBehaviour
{
    public LinkPlayClient client;

    // ============================================================
    // 标记 RPC 方法
    // ============================================================

    // 无参数 RPC
    [LinkPlayRPC]
    public void StartGame()
    {
        Debug.Log("🎮 游戏开始！");
    }

    // 带参数 RPC
    [LinkPlayRPC]
    public void PlayerScoreUpdate(string playerId, int score, int combo)
    {
        Debug.Log($"📊 玩家 {playerId} 得分: {score}, 连击: {combo}");
    }

    // 自定义 RPC 名称
    [LinkPlayRPC(Name = "SyncHealth")]
    public void UpdateHealth(string playerId, float health)
    {
        Debug.Log($"❤️ 玩家 {playerId} 生命值: {health}");
    }

    // ============================================================
    // 调用 RPC
    // ============================================================

    // 开始游戏 → 所有玩家（含自己）
    public async void OnStartGameClicked()
    {
        await client.InvokeRPCAsync(
            methodName: "StartGame",
            targetType: RPCTargetType.AllPlayersInRoom
        );
    }

    // 同步分数 → 除自己外的其他玩家
    public async void SyncScore(string playerId, int score)
    {
        await client.InvokeRPCAsync(
            methodName: "PlayerScoreUpdate",
            parameters: new object[] { playerId, score, 0 },
            targetType: RPCTargetType.Others
        );
    }

    // 报告给房主
    public async void ReportToOwner(string message)
    {
        await client.InvokeRPCAsync(
            methodName: "ReceiveReport",
            parameters: new object[] { message },
            targetType: RPCTargetType.RoomOwner
        );
    }
}
```

## 9.4 玩家位置同步

```csharp
using UnityEngine;
using DLMTP_LinkPlay;
using DLMTP_LinkPlay.CoreSDK;

public class PlayerSync : MonoBehaviour
{
    public LinkPlayClient client;
    private Vector3 _lastPos;
    private float _syncInterval = 0.1f;
    private float _lastSyncTime;

    private void Start()
    {
        client = FindFirstObjectByType<LinkPlayClient>();
        _lastPos = transform.position;
    }

    private void Update()
    {
        if (!client.IsInRoom) return;

        if (Time.time - _lastSyncTime >= _syncInterval)
        {
            if (Vector3.Distance(transform.position, _lastPos) > 0.1f)
            {
                _ = SyncPosition();
                _lastPos = transform.position;
                _lastSyncTime = Time.time;
            }
        }
    }

    private async System.Threading.Tasks.Task SyncPosition()
    {
        var pos = transform.position;
        var rot = transform.rotation.eulerAngles;
        await client.InvokeRPCAsync(
            methodName: "OnRemoteMove",
            parameters: new object[] { client.PlayerId, pos.x, pos.y, pos.z, rot.y },
            targetType: RPCTargetType.Others
        );
    }

    [LinkPlayRPC]
    public void OnRemoteMove(string playerId, float x, float y, float z, float ry)
    {
        if (playerId == client.PlayerId) return;

        var target = GameObject.Find("Player_" + playerId);
        if (target != null)
        {
            Vector3 targetPos = new Vector3(x, y, z);
            target.transform.position = Vector3.Lerp(
                target.transform.position, targetPos, 0.5f);
        }
    }
}
```


