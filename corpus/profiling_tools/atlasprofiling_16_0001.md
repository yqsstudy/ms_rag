---
title: "简介"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0001.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0001.html"
---

# 简介

进行性能调优时，可以使用性能调优工具来采集和分析运行在昇腾AI处理器上的AI任务各个运行阶段的关键性能指标，用户可根据输出的性能数据，快速定位软、硬件性能瓶颈，提升AI任务性能分析的效率。

#### 快速入门

- [离线推理场景推荐使用msprof命令采集，请参见离线推理场景性能分析快速入门](atlasprofiling_16_0003.html#ZH-CN_TOPIC_0000002536038277)。如果当前环境未安装CANN Toolkit开发套件包和ops算子包，则无法使用msprof命令。
- [训练场景推荐直接在AI框架内修改接口参数采集，请参见PyTorch训练场景性能分析快速入门](atlasprofiling_16_0004.html#ZH-CN_TOPIC_0000002536158311)[和TensorFlow训练场景性能分析快速入门](atlasprofiling_16_0005.html#ZH-CN_TOPIC_0000002504198500)。

#### 工具导航

当用户使用msprof命令或使用PyTorch框架接口采集性能数据后，无需使用msprof进行数据解析，这是因为这两种方式在采集后可自动解析；其余采集方式，在采集完成后，需要使用msprof命令进行数据解析。
**表1**工具导航
场景

工具

说明

通用场景

[msprof模型调优工具](atlasprofiling_16_0006.html#ZH-CN_TOPIC_0000002504358336)

msprof模型调优工具不仅可以解析采集到的性能数据，且提供了完整的性能数据采集能力（更多的数据类型）。

不支持采集Python调用栈、PyTorch或MindSpore框架层数据，可使用对应框架接口方式采集。

通用场景

[MSPTI调优工具](atlasprofiling_16_0020.html#ZH-CN_TOPIC_0000002536158321)

MSPTI为通用场景接口，使用MSPTI API开发的Profiling分析工具可以在各种框架的推理和训练场景生效。

MindIE Service推理服务化场景

[msServiceProfiler服务化调优工具](atlasprofiling_16_0025.html#ZH-CN_TOPIC_0000002504198514)

使用msServiceProfiler接口，在MindIE Service推理服务化进程中，采集关键过程的开始和结束时间点，识别关键函数或迭代等信息，记录关键事件，支持多样的信息采集，对性能问题快速定界。

MindSpore框架场景

[MindSpore调优工具](atlasprofiling_16_0117.html#ZH-CN_TOPIC_0000002504198568)

基于MindSpore框架编程时使用。

PyTorch框架场景

[Ascend PyTorch调优工具](atlasprofiling_16_0120.html#ZH-CN_TOPIC_0000002536158381)

基于PyTorch框架编程时使用。

约束：仅支持训练和在线推理场景且需要在AI框架编程时调用Profiling相关代码。

TensorFlow框架场景

[使用TensorFlow框架接口采集性能数据](atlasprofiling_16_0124.html#ZH-CN_TOPIC_0000002536158383)

基于TensorFlow框架编程时使用。

约束：仅支持训练和在线推理场景且需要在AI框架编程时调用Profiling相关代码。

TensorFlow框架场景

[使用环境变量采集性能数据](atlasprofiling_16_0139.html#ZH-CN_TOPIC_0000002536038361)

通过设置特定的环境变量控制Profiling，Profiling配置可以迁移到不同的训练或在线推理的环境变量脚本中执行。

约束：仅支持训练和在线推理场景。

图开发场景

[使用Ascend Graph接口采集性能数据](atlasprofiling_16_0137.html#ZH-CN_TOPIC_0000002504198578)

昇腾Graph开发时使用。

约束：仅支持训练和在线推理场景且需要在Ascend Graph编程中调用Profiling相关接口。

离线推理场景

[使用acl C&C++接口采集性能数据](atlasprofiling_16_0125.html#ZH-CN_TOPIC_0000002504198572)

最灵活的Profiling数据采集方案，提供定制化的性能数据采集能力。

约束：仅支持离线推理场景且需要在应用程序中调用Profiling相关接口。

离线推理场景

[使用acl Python接口采集性能数据](atlasprofiling_16_0131.html#ZH-CN_TOPIC_0000002536038357)

acl API的Python封装版本。

约束：仅支持离线推理场景且需要在应用程序中调用Profiling相关接口。

离线推理场景

[使用acl.json配置文件采集性能数据](atlasprofiling_16_0138.html#ZH-CN_TOPIC_0000002504358414)

配置文件方式，支持Profiling与其他组件的统一配置。

约束：仅支持离线推理场景且需要修改配置文件。
|  |  |  |
| --- | --- | --- |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |