---
title: "IsEnable"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0061.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0061.html"
---

# IsEnable

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

判断是否使能采集数据，当入参级别小于配置的级别时，返回true。

#### 函数原型

```
1
```

```
inline bool IsEnable(Level msgLevel = level)

```
|  |  |
| --- | --- |

#### 参数说明
**表1**参数说明
参数名

输入/输出

说明

msgLevel

输入

[定义的采集等级，参见创建采集配置文件](atlasprofiling_16_0030.html#ZH-CN_TOPIC_0000002504358350)中的profiler_level。
|  |  |  |
| --- | --- | --- |
|  |  |  |

#### 返回值说明

true表示使能数据采集，false表示未使能。
**父主题：**[服务化调优](atlasprofiling_16_0059.html)