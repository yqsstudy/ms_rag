---
title: "msptiActivityGetNextRecord"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0248.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0248.html"
---

# msptiActivityGetNextRecord

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

依次从Activity Buffer中取出数据，每次读取一条Activity数据。

#### 函数原型

```
1
```

```
msptiResult msptiActivityGetNextRecord(uint8_t *buffer, size_t validBufferSizeBytes, msptiActivity **record)

```
|  |  |
| --- | --- |

#### 参数说明
**表1**参数说明
参数名

输入/输出

说明

buffer

输入

设置Activity Buffer的地址。

validBufferSizeBytes

输入

Activity Buffer中记录数据的大小。

record

输出

记录Record数据的地址。
|  |  |  |
| --- | --- | --- |
|  |  |  |
|  |  |  |
|  |  |  |

#### 返回值说明

返回MSPTI_SUCCESS表示成功；Activity Buffer没有更多的Record数据时返回MSPTI_ERROR_MAX_LIMIT_REACHED（表示已取完Activity Buffer中数据），表示失败；Activity Buffer为空时返回MSPTI_ERROR_INVALID_PARAMETER，表示失败。
**父主题：**[Function类型](atlasprofiling_16_0244.html)