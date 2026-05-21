---
title: "msptiActivityDisable"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0247.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0247.html"
---

# msptiActivityDisable

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

停止收集特定类型的Activity Record。该接口支持多次调用，并分别设置不同的msptiActivityKind。

#### 函数原型

```
1
```

```
msptiResult msptiActivityDisable(msptiActivityKind kind)

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

[停止Activity Record的类型，配置为msptiActivityKind](atlasprofiling_16_0259.html#ZH-CN_TOPIC_0000002536038429)的枚举值。
|  |  |  |
| --- | --- | --- |
|  |  |  |

#### 返回值说明

返回MSPTI_SUCCESS表示成功，返回其他值表示失败。
**父主题：**[Function类型](atlasprofiling_16_0244.html)