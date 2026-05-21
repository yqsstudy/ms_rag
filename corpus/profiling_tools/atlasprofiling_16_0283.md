---
title: "msptiUnsubscribe"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0283.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0283.html"
---

# msptiUnsubscribe

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

向MSPTI注销当前订阅者。

#### 函数原型

```
1
```

```
msptiResult msptiUnsubscribe(msptiSubscriberHandle subscriber)

```
|  |  |
| --- | --- |

#### 参数说明
**表1**参数说明
参数名

输入/输出

说明

**subscriber**

输入

订阅者句柄。
|  |  |  |
| --- | --- | --- |
|  |  |  |

#### 返回值说明

返回MSPTI_SUCCESS表示成功，用户为空或未初始化时返回MSPTI_ERROR_INVALID_PARAMETER，表示失败。
**父主题：**[Function类型](atlasprofiling_16_0281.html)