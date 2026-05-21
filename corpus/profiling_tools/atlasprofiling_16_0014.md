---
title: "延迟采集性能数据"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0014.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0014.html"
---

# 延迟采集性能数据

使用msprof命令行进行性能数据采集时，可以通过本节介绍的--delay和--duration参数配置采集的持续时间和延迟采集功能。

[延迟采集场景下不支持动态采集性能数据](atlasprofiling_16_0013.html#ZH-CN_TOPIC_0000002504198506)。

#### 支持的型号

Atlas 200I/500 A2 推理产品

Atlas 推理系列产品

Atlas 训练系列产品

Atlas A2 训练系列产品/Atlas A2 推理系列产品

Atlas A3 训练系列产品/Atlas A3 推理系列产品

#### 注意事项

- 请确保AI任务能在运行环境中正常运行。
- [请确保完成使用前准备](atlasprofiling_16_0002.html#ZH-CN_TOPIC_0000002504358330)。

不支持采集Python调用栈、PyTorch或MindSpore框架层数据，可使用对应框架接口方式采集。

#### 命令示例

以运行用户登录CANN Toolkit开发套件包和ops算子包所在环境，执行以下命令采集性能数据。命令示例如下：
****************
```
msprof --delay=3 --duration=3 /home/projects/MyApp/out/main
```

**仅当采集AI任务运行性能数据时支持启用延迟采集能力，必须传入用户程序，与--dynamic**参数不能同时配置。

#### 参数说明
**表1**参数说明
参数

描述

**可选/必选**

--delay

按设定时间延迟采集性能数据，范围[1, 4294967295]，单位s，默认值0。若配置的时间超过了AI任务的执行时间，在AI任务执行期间不会启动采集。

可选

--duration

性能数据采集的持续时间，范围[1, 4294967295]，单位s，默认未配置，即随采集开始持续到任务结束，自动停止采集。若配置了--delay参数，则duration从delay结束的时刻开始计时。

可选
|  |  |  |
| --- | --- | --- |
|  |  |  |
|  |  |  |
**父主题：**[性能数据采集和自动解析](atlasprofiling_16_0007.html)