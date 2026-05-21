---
title: "MetricScopeAsReqID"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0067.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0067.html"
---

# MetricScopeAsReqID

#### 产品支持情况

产品

是否支持

Atlas 800I A2 推理产品

√

Atlas 200T A2 Box16 异构子框

√

Atlas 300I Duo 推理卡+Atlas 800 推理服务器（型号：3000）

√

注：暂不支持其他产品。
|  |  |
| --- | --- |
|  |  |
|  |  |
|  |  |
|  |  |

#### 功能说明

定义一个指标类的作用范围为请求级别。

#### 函数原型

```
1
```

```
inline Profiler &MetricScopeAsReqID()

```
|  |  |
| --- | --- |

#### 参数说明

无

#### 返回值说明

Profiler&返回当前对象，支持链式调用。
**父主题：**[服务化调优](atlasprofiling_16_0059.html)