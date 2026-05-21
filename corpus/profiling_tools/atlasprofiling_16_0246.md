---
title: "msptiActivityEnable"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0246.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0246.html"
---

# msptiActivityEnable

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

使能MSPTI采集指定Kind的Activity数据。

收集特定类型的Activity Record。支持该接口的多次调用，并分别设置不同的msptiActivityKind，MSPTI可以采集不同类型的Activity数据。

#### 函数原型

```
1
```

```
msptiResult msptiActivityEnable(msptiActivityKind kind)

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

[Activity Record的类型，配置为msptiActivityKind](atlasprofiling_16_0259.html#ZH-CN_TOPIC_0000002536038429)的枚举值。
|  |  |  |
| --- | --- | --- |
|  |  |  |

#### 返回值说明

返回MSPTI_SUCCESS表示成功，返回其他值表示失败。
**父主题：**[Function类型](atlasprofiling_16_0244.html)