# DLMTP_LinkPlay SDK 文档站

> 基于 Docsify 构建的 Unity 联机客户端 SDK 文档站点

本仓库是 [DLMTP_LinkPlay](https://github.com/SoraSushi776/DLMTP_LinkPlay_Docs) SDK 的文档站点，使用 [Docsify](https://docsify.js.org/) 构建，无需编译即可部署。

## 快速开始

### 本地预览

```bash
# 安装 docsify-cli
npm i docsify-cli -g

# 启动本地服务器
docsify serve .

# 访问 http://localhost:3000
```

### 部署到 GitHub Pages

1. 将本仓库推送到 GitHub
2. 在仓库 Settings → Pages 中选择 `main` 分支，根目录部署
3. 访问 `https://<用户名>.github.io/<仓库名>/`

## 文档结构

```
├── index.html               # Docsify 入口
├── _sidebar.md              # 侧边栏导航
├── _coverpage.md            # 封面页
├── .nojekyll                # GitHub Pages 禁用 Jekyll
├── index.md                 # 首页（项目概述）
├── getting-started.md       # 快速开始
├── enums.md                 # 枚举与常量
├── rpc-attribute.md         # RPC 属性
├── data-models.md           # 数据模型
├── client.md                # 核心客户端
├── message-handler.md       # 消息处理器
├── protocol.md              # 协议格式
├── examples.md              # 完整使用示例
├── game-components.md       # Game 组件
├── faq.md                   # 常见问题
└── assets/
    ├── css/
    │   └── style.css        # 自定义样式
```

## 许可

[MIT](LICENSE)
