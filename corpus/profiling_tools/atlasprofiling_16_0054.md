---
title: "启动Trace转发进程"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0054.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0054.html"
---

# 启动Trace转发进程

#### 功能说明

启动Trace转发进程。

#### 注意事项

重试机制：单条请求发送失败（默认重发6次），Trace转发进程不再接受后续的Trace数据，直到该请求发送成功才恢复数据转发功能。

#### 命令格式

```
python -m ms_service_profiler.trace [--log-level]
```

options参数说明请参见参数说明。

#### 参数说明
**表1**参数说明
**参数**

说明

**是否必选**

--log-level

设置日志级别，取值为：

- debug：调试级别。该级别的日志记录了调试信息，便于开发人员或维护人员定位问题。
- info：正常级别。记录工具正常运行的信息。默认值。
- warning：警告级别。记录工具和预期的状态不一致，但不影响整个进程运行的信息。
- error：一般错误级别。
- fatal：严重错误级别。
- critical：致命错误级别。

否
|  |  |  |
| --- | --- | --- |
|  |  |  |

#### 使用示例

使用默认配置启动Trace转发进程。命令如下：

```
python -m ms_service_profiler.trace
```

启动Trace转发进程使用的用户需要和启动MindIE Motor服务的用户一致，且在同网络命名空间中（同docker或同host）。

#### 输出说明
转发进程启动成功时打印示例如下：
```
2025-11-27 18:46:42,737 - 23410 - msServiceProfiler - INFO - Start http/protobuf exporter, endpoint: http://localhost:4318/v1/traces
2025-11-27 18:46:42,737 - 23410 - msServiceProfiler - INFO - Start socket server success, listen addr: OTLP_SOCKET
2025-11-27 18:46:42,737 - 23410 - msServiceProfiler - INFO - Start scheduler task: interval 1s
2025-11-27 18:46:42,738 - 23410 - msServiceProfiler - INFO - Start OTLPForwarderService success, running...
```
**父主题：**[数据采集](atlasprofiling_16_0051.html)