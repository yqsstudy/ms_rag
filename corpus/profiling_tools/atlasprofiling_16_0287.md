---
title: "msptiCallbackFunc"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0287.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0287.html"
---

# msptiCallbackFunc

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

x

Atlas 训练系列产品

x
|  |  |
| --- | --- |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |

#### 功能说明

回调函数类型。

#### 函数原型

```
1
```

```
typedef void (*msptiCallbackFunc)(void *userdata, msptiCallbackDomain domain, msptiCallbackId cbid, const msptiCallbackData *cbdata)

```
|  |  |
| --- | --- |

#### 参数说明
**表1**参数说明
参数名

输入/输出

说明

userdata

输入

用户侧数据地址。

domain

输入

当前回调触发所属的domain域。

cbid

输入

当前回调触发所属的ID。

cbdata

输入

[当前回调触发附带信息。domain为MSPTI_CB_DOMAIN_RUNTIME时，cbdata类型为msptiCallbackData](atlasprofiling_16_0296.html#ZH-CN_TOPIC_0000002536158475)。
|  |  |  |
| --- | --- | --- |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |

#### 返回值说明

无
**父主题：**[Typedef类型](atlasprofiling_16_0286.html)