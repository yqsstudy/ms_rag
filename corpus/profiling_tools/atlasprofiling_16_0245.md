---
title: "msptiActivityRegisterCallbacks"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0245.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0245.html"
---

# msptiActivityRegisterCallbacks

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

向MSPTI注册回调函数，用于Activity Buffer处理。当Activity Buffer空间不足时会调用funcBufferRequested函数申请内存；Activity Buffer空间占满时调用funcBufferCompleted函数通知用户消费Activity数据，并释放Activity Buffer空间。

#### 函数原型

```
1
```

```
msptiResult msptiActivityRegisterCallbacks(msptiBuffersCallbackRequestFunc funcBufferRequested, msptiBuffersCallbackCompleteFunc funcBufferCompleted)

```
|  |  |
| --- | --- |

#### 参数说明
**表1**参数说明
参数名

输入/输出

说明

funcBufferRequested

输入

Activity Buffer内存申请函数。

funcBufferCompleted

输入

Activity Buffer数据消费和内存释放函数。
|  |  |  |
| --- | --- | --- |
|  |  |  |
|  |  |  |

#### 返回值说明

返回MSPTI_SUCCESS表示成功，funcBufferRequested或funcBufferCompleted为NULL时返回MSPTI_ERROR_INVALID_PARAMETER，表示失败。
**父主题：**[Function类型](atlasprofiling_16_0244.html)