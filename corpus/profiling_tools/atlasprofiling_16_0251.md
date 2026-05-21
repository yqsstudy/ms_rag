---
title: "msptiActivityPushExternalCorrelationId"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0251.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0251.html"
---

# msptiActivityPushExternalCorrelationId

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

为调用线程推送外部关联ID。

[此函数通知MSPTI调用线程进入外部API区域。当在外部API区域内创建MSPTI活动API记录并且启用了MSPTI_ACTIVITY_KIND_EXTERNAL_CORRELATION](atlasprofiling_16_0259.html#ZH-CN_TOPIC_0000002536038429)[时，对于每个msptiExternalCorrelationKind](atlasprofiling_16_0265.html#ZH-CN_TOPIC_0000002504198644)[，活动API记录的前面将有一个msptiActivityExternalCorrelation](atlasprofiling_16_0276.html#ZH-CN_TOPIC_0000002536158465)记录。

#### 函数原型

```
1
```

```
msptiResult msptiActivityPushExternalCorrelationId(msptiExternalCorrelationKind kind, uint64_t id)

```
|  |  |
| --- | --- |

#### 参数说明
**表1**参数说明
参数名

输入/输出

说明

kind

输入

[关联的外部API活动类型，当前有效kind为xxx_CUSTOM0。调用枚举类msptiExternalCorrelationKind](atlasprofiling_16_0265.html#ZH-CN_TOPIC_0000002504198644)。

id

输入

由外部组件生成的关联ID，用于push到MSPTI指定的stack里。
|  |  |  |
| --- | --- | --- |
|  |  |  |
|  |  |  |

#### 返回值说明

返回MSPTI_SUCCESS表示成功，外部关联类型无效时返回MSPTI_ERROR_INVALID_PARAMETER和外部关联ID栈空时出栈返回MSPTI_ERROR_QUEUE_EMPTY，表示失败。
**父主题：**[Function类型](atlasprofiling_16_0244.html)