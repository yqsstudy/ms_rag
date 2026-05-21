---
title: "发送请求"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0055.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0055.html"
---

# 发送请求

当前建议使用/v1/chat/completions及/v1/completions接口发送请求。且这两个接口的HTTP请求头中需要添加“开启采样”信息。当前支持添加“开启采样”的HTTP请求头格式如下：

- W3C Trace Context (traceparent)
- B3 Single Header (单一头格式)
- B3 Multiple Headers (多头格式)

HTTP请求头需要添加的内容格式详细配置介绍如下：

#### W3C Trace Context (traceparent)

例如：

```
traceparent: 00-0af7651916cd43dd8448eb211c80319c-b7ad6b7169203331-01
```
**表1**W3C Trace Context (traceparent)
字段

位置

长度

含义

可选/必选

version

前2位

2字符

协议版本，目前固定为00

必选

trace-id

3~34位

32字符

全局Trace ID（16字节，32个十六进制字符），唯一标识整个分布式调用链

必选

parent-id

36~51位

16字符

父Span ID（8字节，16个十六进制字符），标识当前操作的直接上游

必选

trace-flags

53~54位

2字符

**Trace标志，目前只使用最低位：01=采样，00=不采样**

必选
|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |
|  |  |  |  |  |
|  |  |  |  |  |
|  |  |  |  |  |

#### B3 Single Header（单一头格式）

例如：

```
b3: 0af7651916cd43dd8448eb211c80319c-b7ad6b7169203331-1-0000000000000001
```
**表2**B3 Single Header（单一头格式）
字段

字符位置

含义

格式

取值说明

可选/必选

TraceId

1~32位

全局Trace ID

32个十六进制字符

唯一标识整个分布式调用链

必选

SpanId

34~49位

当前Span ID

16个十六进制字符

标识当前服务操作的唯一ID

必选

Sampled

51位

采样决策

1个字符

**1=采样**

**0=不采样**

必选

ParentSpanId

53~68位

父Span ID

16个十六进制字符

可选字段，标识直接上游Span

可选
|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |
|  |  |  |  |  |  |
|  |  |  |  |  |  |
|  |  |  |  |  |  |

#### B3 Multiple Headers（多头格式）

例如：

```
X-B3-TraceId: 0af7651916cd43dd8448eb211c80319c
X-B3-SpanId: b7ad6b7169203331
X-B3-Sampled: 1
```
**表3**B3 Multiple Headers（多头格式）
字段名称

含义

格式

取值

作用

可选/必选

X-B3-TraceId

全局Trace ID

32个十六进制字符（16字节）

任意32位十六进制字符串

唯一标识整个分布式调用链，所有相关服务共享同一个TraceId

必选

X-B3-SpanId

当前Span ID

16个十六进制字符（8字节）

任意16位十六进制字符串

标识当前服务操作的唯一ID，每个Span都有独立的SpanId

必选

X-B3-Sampled

采样决策

字符串

**1 = 采样**

**0 = 不采样**

控制是否记录Trace数据到后端系统，避免产生过多性能开销

必选
|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |
|  |  |  |  |  |  |
|  |  |  |  |  |  |

#### 执行发送请求

发送的HTTP请求头中必须添加上述三种HTTP请求头格式的其中一种，才可以执行发送请求并开启Trace数据监控功能。其中配置的SpanId和TraceId会作为每个请求的索引。

以在HTTP请求头添加W3C Trace Context (traceparent)格式为例，执行发送请求命令如下：

```
curl http://127.0.0.1:1025/v1/chat/completions \
-X POST \
-H "Content-Type: application/json" -H "traceparent: 04-01f92f3577b34da6a3ce929d0e0e4703-00f067aa0ba90203-01" \
-d '{
"model": "qwen",
"messages": [
{"role": "user", "content": "用Python写一个简单的冒泡排序算法："}
],
"max_tokens": 300,
"temperature": 0.5,
"stream": false }'
```
**父主题：**[数据采集](atlasprofiling_16_0051.html)