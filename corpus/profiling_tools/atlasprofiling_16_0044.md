---
title: "自定义添加采集代码"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0044.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0044.html"
---

# 自定义添加采集代码

MindIE Motor推理服务化框架中默认已添加性能数据采集代码，当前步骤可选。

[若需要自定义采集更多性能数据，可以参照如下示例代码对服务化框架中的性能采集代码进行修改，可以使用的接口请参见服务化调优](atlasprofiling_16_0059.html#ZH-CN_TOPIC_0000002536038319)[或服务化调优](atlasprofiling_16_0100.html#ZH-CN_TOPIC_0000002536158371)。

下列示例使用C++接口。

Span类数据采集：

```
1
2
3
4
5
6
7
8
```

```
// 记录执行开始结束时间
auto span = PROF(INFO, SpanStart("exec"));

...
// 用户执行代码

PROF(span.SpanEnd());
// 也可以不调用SpanEnd函数，在析构时会自动调用SpanEnd结束采集

```
|  |  |
| --- | --- |

Event类数据采集：

```
1
2
```

```
// 记录缓存交换事件
PROF(INFO, Event("cacheSwap"));

```
|  |  |
| --- | --- |

Metric类数据采集：

```
1
2
3
4
5
6
```

```
// 普通数据采集：利用率50%
PROF(INFO, Metric("usage", 0.5).Launch());
// 数据的增量采集：请求数量 + 1
PROF(INFO, MetricInc("reqSize", 1).Launch());
// 定义采集数据的范围（默认是全局）：第3个队列的当前大小是14
PROF(INFO, Metric("queueSize", 14).MetricScope("queue", 3).Launch());

```
|  |  |
| --- | --- |

Link类数据采集：

```
1
2
3
```

```
// 关联不同的资源，实际应用时不同模块对同一个请求使用不同的编号，将两个系统的编号关联起来
// reqID_SYS1和reqID_SYS2对应不同的系统编号
PROF(INFO, Link("reqID_SYS1", "reqID_SYS2"));

```
|  |  |
| --- | --- |

属性数据采集：

```
1
2
3
4
5
6
```

```
// 以上调用，都可以在结束前，在中间使用链式添加属性
PROF(INFO, Attr("attr", "attrValue").Attr("numAttr", 66.6).Event("test"));
// 属性可以自定义采集级别
PROF(INFO, Attr<msServiceProfiler::VERBOSE>("verboseAttr", 1000).Event("test"));
// 其他属性如：Domain(域)、Res(资源，一般是请求ID)等也可以使用链式进行添加
PROF(INFO, Domain("http").Res(reqId).Attr("attr", "attrValue").Event("test"));

```
|  |  |
| --- | --- |
**父主题：**[扩展功能](atlasprofiling_16_0043.html)