---
title: "总体介绍"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0132.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0132.html"
---

# 总体介绍

本章节提供离线推理场景下，如何通过API方式采集性能数据，支持以下实现方式：
**表1**采集方式
采集方式

说明

方式一：采集并落盘性能数据

将采集到的性能数据写入文件，再使用msprof工具解析该文件，并展示性能分析数据。

方式二：使用msproftx扩展接口采集并落盘性能数据

当用户需要定位应用程序或上层框架程序的性能瓶颈时，可在Profiling采集进程内（acl.prof.start接口、acl.prof.stop接口之间）调用msproftx，开启记录应用程序执行期间特定事件发生的时间跨度，并将数据写入性能数据文件，再使用msprof工具解析该文件，并导出展示性能分析数据。

方式三：订阅算子信息

将采集到的性能数据解析后写入管道，由用户读入内存，再由用户调用API获取性能数据。

[注：接口详细说明，请参见“Profiling数据采集](https://www.hiascend.com/document/detail/zh/canncommercial/850/API/appdevgapi/aclpythondevg_01_0847.html)”。
|  |  |
| --- | --- |
|  |  |
|  |  |
|  |  |
|  |  |

- 使用接口进行性能数据采集，须完成应用工程开发、编译和运行。
- 方式一和方式二不能与方式三交叉调用。
**父主题：**[使用acl Python接口采集性能数据](atlasprofiling_16_0131.html)