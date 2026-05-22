---
layout: default
title: Game 组件
nav_order: 11
---

# 11. Game 组件（LinkPlayContent / PingDisplay）

SDK 在 `DLMTP_LinkPlay.Game` 命名空间下提供了两个开箱即用的 UI 组件。

## 11.1 LinkPlayContent — 大厅入口按钮

`LinkPlayContent` 是一个 MonoBehaviour 脚本，挂载在大厅页面的"进入联机"按钮上。点击按钮后自动连接联机服务器，加入大厅并切换页面。

### Inspector 属性

| 字段 | 类型 | 说明 |
|------|------|------|
| `linkPlayClient` | `LinkPlayClient` | 联机客户端引用（留空可在编辑器中点击「自动绑定引用」按钮查找） |
| `linkPlayPage` | `ShowCanvas` | 联机大厅页面（LinkPlay_Page），加入成功时显示 |
| `lobbyPage` | `HideCanvas` | 大厅主页面（Lobby_Page），加入成功后隐藏 |
| `linkPlayButton` | `Button` | 按钮自身引用（用于禁用交互防止重复点击） |
| `autoFetchRoomList` | `bool` | 加入大厅后是否自动获取房间列表（默认 `true`） |

### 工作流程

```csharp
// 内部状态机
OnClickJoinLobby()
  ├─ 如果正在连接中 → 忽略
  ├─ 如果 linkPlayClient == null → 提示错误
  ├─ 如果 IsInLobby 或 IsConnected → 直接显示 LinkPlay_Page
  └─ 否则：
       ├─ 禁用按钮交互
       ├─ 显示 WaitingCanvas "正在加入联机大厅..."
       ├─ await linkPlayClient.ConnectAsync()
       ├─ 成功 → 等待 OnJoinedLobby 回调
       │   ├─ 隐藏 WaitingCanvas
       │   ├─ 显示 LinkPlay_Page，隐藏 Lobby_Page
       │   ├─ 自动获取房间列表（如启用）
       │   └─ 播放联机大厅音乐并提示成功
       └─ 失败 → 隐藏 WaitingCanvas，启用按钮，提示错误
```

### 编辑器工具

在 Inspector 中点击「自动绑定引用」按钮可自动查找场景中的 `LinkPlayClient`、`ShowCanvas`、`HideCanvas` 和 `Button` 引用。

---

## 11.2 PingDisplay — 网络延迟显示

`PingDisplay` 是一个 MonoBehaviour 脚本，在屏幕右下角使用 `OnGUI` 渲染当前网络延迟。

### Inspector 属性

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `linkPlayClient` | `LinkPlayClient` | 自动查找 | 联机客户端引用 |
| `fontSize` | `int` | `20` | 字体大小 |
| `offsetX` | `float` | `30` | 距离屏幕右边缘偏移（像素） |
| `offsetY` | `float` | `30` | 距离屏幕底边缘偏移（像素） |

### 延迟颜色分级

| 延迟范围 | 颜色 | 含义 |
|----------|------|------|
| `-1`（未测量） | 灰色 | 尚未收到首次 pong |
| `< 50 ms` | 绿色 | 优秀 |
| `50 ~ 99 ms` | 黄色 | 良好 |
| `100 ~ 199 ms` | 橙色 | 一般 |
| `≥ 200 ms` | 红色 | 较差 |

### 工作原理

```
Start() → 自动查找 LinkPlayClient → 绑定 OnPingUpdated 事件
   ↓
LinkPlayClient 每次收到 pong → 更新 CurrentPingMs → 触发 OnPingUpdated(callback)
   ↓
PingDisplay.OnPingUpdated(pingMs) → 存储 _currentPing
   ↓
OnGUI() → 绘制半透明背景 + 延迟文本（根据值着色）
```

### 显示效果

```
┌──────────────────────┐
│   延迟: 32 ms        │  ← 绿色背景
└──────────────────────┘
```

每帧在 `OnGUI` 中绘制，使用 `Texture2D` 作为半透明背景，文本右对齐显示。

---

[← 常见问题](faq.md) | [返回首页](index.md)
