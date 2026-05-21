---
title: "msptiActivityPopExternalCorrelationId"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0252.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0252.html"
---

# msptiActivityPopExternalCorrelationId

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

为调用线程拉取外部关联ID。

#### 函数原型

```
1
```

```
msptiResult msptiActivityPopExternalCorrelationId(msptiExternalCorrelationKind kind, uint64_t *lastId)

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

关联的外部API活动类型，当前有效kind为xxx_CUSTOM0。

lastId

输入

MSPTI会pop出Stack里面的ID，并写到lastId里。
|  |  |  |
| --- | --- | --- |
|  |  |  |
|  |  |  |

#### 返回值说明

返回MSPTI_SUCCESS表示成功，外部关联类型无效时返回MSPTI_ERROR_INVALID_PARAMETER，表示失败。
**父主题：**[Function类型](atlasprofiling_16_0244.html)