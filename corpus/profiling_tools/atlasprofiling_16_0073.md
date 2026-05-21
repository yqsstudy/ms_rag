---
title: "ArrayResource"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0073.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0073.html"
---

# ArrayResource

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

添加数组类资源的关键属性。

#### 函数原型

```
1
2
3
```

```
template <typename T>
inline Profiler &ArrayResource(const T &startIter, const T &endIter,
    typename ArrayCollectorHelper<Profiler<level>, T>::AttrCollectCallback callback)

```
|  |  |
| --- | --- |

#### 参数说明
**表1**参数说明
参数名

输入/输出

说明

startIter

输入

任意的迭代器开始。

endIter

输入

任意的迭代器结束。

callback

输入

元素属性提取回调函数。
|  |  |  |
| --- | --- | --- |
|  |  |  |
|  |  |  |
|  |  |  |

#### 返回值说明

Profiler&返回当前对象，支持链式调用。
**父主题：**[服务化调优](atlasprofiling_16_0059.html)