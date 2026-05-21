---
title: "mstxDomainMarkA"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/API/mstxAPIReference/msprof_tx_0008.html"
date_collected: "2026-05-04"
category: "mstx_api"
original_path: "zh/mindstudio/830/API/mstxAPIReference/msprof_tx_0008.html"
---

# mstxDomainMarkA

#### 产品支持情况

产品

是否支持

Atlas A3 训练系列产品/Atlas A3 推理系列产品

√

Atlas A2 训练系列产品/Atlas A2 推理系列产品

√

Atlas 200I/500 A2 推理产品

√

Atlas 推理系列产品

√

Atlas 训练系列产品

√
|  |  |
| --- | --- |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |

#### 功能说明

在指定的domain内，标记瞬时事件。

如果传入的domain已被销毁，日志打印告警提示，接口不再执行打点流程。

#### 函数原型

```
1
```

```
void mstxDomainMarkA(mstxDomainHandle_t domain, const char *message, aclrtStream stream)

```
|  |  |
| --- | --- |

#### 参数说明
**表1**参数说明
参数名

输入/输出

说明

domain

输入

指定的domain句柄。

message

输入

打点携带信息字符串指针。

传入的message字符串长度要求：

- MSPTI场景：不能超过255字节。
- 非MSPTI场景（例如msprof命令行、Ascend PyTorch Profiler）：不能超过156字节。

stream

输入

用于执行打点任务的stream。

- 配置为nullptr时，只标记Host侧的瞬时事件。
- 配置为有效的stream时，标记Host侧和对应Device侧的瞬时事件。
|  |  |  |
| --- | --- | --- |
|  |  |  |
|  |  |  |
|  |  |  |

#### 返回值

无