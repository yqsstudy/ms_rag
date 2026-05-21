---
title: "总体说明"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0081.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0081.html"
---

# 总体说明

#### 接口简介

Trace模块提供推理服务化性能数据采集（C++）接口，用于Trace数据监控。

[Trace接口功能介绍和使用示例请参见msServiceProfiler Trace数据监控](atlasprofiling_16_0048.html#ZH-CN_TOPIC_0000002536158341)。

头文件：${INSTALL_DIR}/include/msServiceProfiler/Tracer.h

库文件：${INSTALL_DIR}/lib64/libms_service_profiler.so

${INSTALL_DIR}请替换为CANN软件安装后文件存储路径。以root用户安装为例，则安装后文件存储路径为：/usr/local/Ascend/cann。

#### 接口列表

具体接口如下：
**表1**Trace API（C++）
接口

说明

[TraceContext类](atlasprofiling_16_0083.html#ZH-CN_TOPIC_0000002536038331)

Trace上下文管理类，负责管理线程级别的Trace信息。

[GetTraceCtx](atlasprofiling_16_0084.html#ZH-CN_TOPIC_0000002536158363)

获取当前线程的Trace上下文实例。

[addResAttribute](atlasprofiling_16_0085.html#ZH-CN_TOPIC_0000002504198552)

添加资源属性（全局属性）。

[ExtractAndAttach](atlasprofiling_16_0086.html#ZH-CN_TOPIC_0000002504358388)

解析HTTPTrace信息并附加到当前上下文。

[Attach](atlasprofiling_16_0087.html#ZH-CN_TOPIC_0000002536038333)

附加Trace信息到当前上下文。

[Unattach](atlasprofiling_16_0088.html#ZH-CN_TOPIC_0000002536158365)

解除指定索引的Trace上下文。

[GetCurrent](atlasprofiling_16_0089.html#ZH-CN_TOPIC_0000002504198554)

获取当前Trace上下文信息。

[Span类](atlasprofiling_16_0090.html#ZH-CN_TOPIC_0000002504358390)

跨度类，表示一个具体的操作或请求。

[Span](atlasprofiling_16_0091.html#ZH-CN_TOPIC_0000002536038337)

创建一个跨度。

[Activate](atlasprofiling_16_0092.html#ZH-CN_TOPIC_0000002536158367)

激活跨度并开始计时。

[SetAttribute](atlasprofiling_16_0093.html#ZH-CN_TOPIC_0000002504198556)

设置跨度属性。

[SetStatus](atlasprofiling_16_0094.html#ZH-CN_TOPIC_0000002504358392)

设置跨度状态。

[End](atlasprofiling_16_0095.html#ZH-CN_TOPIC_0000002536038339)

结束跨度。

[Tracer类](atlasprofiling_16_0096.html#ZH-CN_TOPIC_0000002536158369)

提供创建跨度的接口。

[StartSpanAsActive](atlasprofiling_16_0097.html#ZH-CN_TOPIC_0000002504198558)

创建并激活一个跨度。

[IsEnable](atlasprofiling_16_0098.html#ZH-CN_TOPIC_0000002504358394)

检查Trace功能是否启用。
|  |  |
| --- | --- |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
**父主题：**[Trace数据监控](atlasprofiling_16_0080.html)