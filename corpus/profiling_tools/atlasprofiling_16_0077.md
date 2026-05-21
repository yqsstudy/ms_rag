---
title: "ArrayAttr"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0077.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0077.html"
---

# ArrayAttr

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

通过回调函数自定义添加数组属性。

#### 函数原型

```
1
2
```

```
template <Level levelAttr = level, typename T>
Profiler &ArrayAttr(const char *attrName, const T &startIter, const T &endIter, typename ArrayCollectorHelper<Profiler<level>, T>::AttrCollectCallback callback)

```
|  |  |
| --- | --- |

#### 参数说明
**表1**参数说明
参数名

输入/输出

说明

attrName

输入

属性名。

startIter

输入

任意的迭代器开始。

endIter

输入

任意的迭代器结束。

callback

输入

回调函数第一个入参是当前对象，可以调用它添加属性，第二个入参是当前迭代，可以用它获取需要记录的属性内容。
|  |  |  |
| --- | --- | --- |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |

#### 返回值说明

Profiler&返回当前对象，支持链式调用。
**父主题：**[服务化调优](atlasprofiling_16_0059.html)