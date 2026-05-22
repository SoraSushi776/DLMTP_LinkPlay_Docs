---
layout: default
title: RPC 属性
nav_order: 4
---

# 4. RPC 属性（LinkPlayRPC）

`[LinkPlayRPC]` 是一个方法级别的 Attribute，用于标记可被远程调用的方法。

## 定义

```csharp
[AttributeUsage(AttributeTargets.Method, AllowMultiple = false, Inherited = true)]
public class LinkPlayRPC : Attribute
```

## 属性

| 属性名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `Name` | `string` | 否 | 自定义 RPC 方法名。不设置时默认使用 C# 方法名。设置后远程调用时需使用此名称。 |
| `Description` | `string` | 否 | RPC 方法描述，仅用于文档说明。 |

## 使用规则

- ✅ 可标记在 `public` / `private` / `protected` 方法上
- ✅ 方法必须位于继承自 `MonoBehaviour` 的类中
- ✅ 方法所在的 `GameObject` 必须为 **active in hierarchy**
- ✅ 参数支持：`int`、`float`、`double`、`long`、`bool`、`string`、`Dictionary<string, object>`
- ❌ 不支持：`GameObject`、`Transform` 等 Unity 特有类型

---

[← 枚举与常量](enums.md) | [下一章：数据模型 →](data-models.md)
