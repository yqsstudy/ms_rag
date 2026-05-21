---
title: "SpanStart"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0062.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0062.html"
---

# SpanStart

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

记录一个过程的开始节点。

#### 函数原型

```
1
```

```
Profiler &SpanStart(const char *spanName, bool autoEnd = true)

```
|  |  |
| --- | --- |

#### 参数说明
**表1**参数说明
参数名

输入/输出

说明

spanName

输入

区间名字。

autoEnd

输入

（可选）是否自动调用End，默认自动调用。
|  |  |  |
| --- | --- | --- |
|  |  |  |
|  |  |  |

#### 返回值说明

Profiler&返回当前对象，支持链式调用。
**父主题：**[服务化调优](atlasprofiling_16_0059.html)