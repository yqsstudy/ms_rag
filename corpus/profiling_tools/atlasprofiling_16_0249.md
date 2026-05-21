---
title: "msptiActivityFlushAll"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0249.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0249.html"
---

# msptiActivityFlushAll

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

用户（订阅者）调用回调函数，将缓冲区中的所有Activity数据写入用户内存。

该接口为同步接口，在全部Activity数据消费后结束，推荐在子线程中调用。

#### 函数原型

```
1
```

```
msptiResult msptiActivityFlushAll(uint32_t flag)

```
|  |  |
| --- | --- |

#### 参数说明
**表1**参数说明
参数名

输入/输出

说明

flag

输入

设置Flush的行为。当前该参数的功能暂不支持。
|  |  |  |
| --- | --- | --- |
|  |  |  |

#### 返回值说明

返回MSPTI_SUCCESS表示成功，MSPTI未被初始化时返回MSPTI_ERROR_NOT_INITIALIZED，表示失败。
**父主题：**[Function类型](atlasprofiling_16_0244.html)