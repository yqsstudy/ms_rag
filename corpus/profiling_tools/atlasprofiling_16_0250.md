---
title: "msptiActivityFlushPeriod"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0250.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0250.html"
---

# msptiActivityFlushPeriod

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

以设定的时间，周期性检查是否有已满的buffer，若有则进行上报。

#### 函数原型

```
1
```

```
msptiResult msptiActivityFlushPeriod(uint32_t time)

```
|  |  |
| --- | --- |

#### 参数说明
**表1**参数说明
参数名

输入/输出

说明

time

输入

检查已满buffer的执行周期，单位ms。设置为0时，表示关闭定期检查已满buffer的功能。

建议用户不要将间隔设为一个较小的值，以防频繁检查。
|  |  |  |
| --- | --- | --- |
|  |  |  |

#### 返回值说明

返回MSPTI_SUCCESS表示成功，返回其他值表示失败。
**父主题：**[Function类型](atlasprofiling_16_0244.html)