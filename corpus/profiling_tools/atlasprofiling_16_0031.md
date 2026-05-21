---
title: "执行采集"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0031.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0031.html"
---

# 执行采集

服务化性能数据采集支持运行时动态启停。操作步骤如下：

1. 配置环境变量，指定采集配置文件ms_service_profiler_config.json。

```
export SERVICE_PROF_CONFIG_PATH="./ms_service_profiler_config.json"
```

  - 若环境变量配置路径下不存在json配置文件，会在路径下自动创建默认配置的json文件，且enable开关为0关闭状态，需要在运行MindIE Motor服务后执行3，配置enable开关为1，开启采集任务。
  - 若环境变量配置路径下已存在同名的json文件，则不会创建json文件。

2. 运行MindIE Motor服务。
3. 开启采集任务。

**重新开启一个命令行窗口，用户可以通过修改ms_service_profiler_config.json配置中的“enable**”字段，实时切换数据采集功能的开启和关闭。开启和关闭采集功能时产生相应日志，见动态启停说明。

采集完成后，Profiling性能数据落盘在ms_service_profiler_config.json中prof_dir参数指定的路径下。


- 多机多卡场景可使用Samba工具实现共享配置文件，以此实现对多机多卡场景的性能数据采集。其中多机多卡场景执行采集步骤与上文一致，但需要每个节点分别启动MindIE Motor服务。Samba为第三方工具，请用户自行查找对应使用指导，或使用其他支持配置共享目录的工具。
- [服务化调优工具的acl_task_time开关与msprof工具的动态采集功能存在冲突，建议不要同时使用。msprof工具的动态采集功能相关介绍请参见《性能调优工具用户指南](https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0001.html)》。

#### 动态启停说明

动态启停指在启动采集任务后，执行采集操作过程中可以随时启动和暂停采集。

动态启停场景主要为以下三种：

- 关闭到开启。启动MindIE Motor服务前，json配置文件中“enable”字段设置为0，运行后修改文件中“enable”字段为1，日志中打印开启采集功能的相关信息：


- 开启到关闭。启动MindIE Motor服务前，json配置文件中“enable”字段设置为1，运行后修改文件中“enable”字段为0，日志中打印关闭采集功能的相关信息：


- 修改json配置文件内容，但“enable”字段未更改，采集功能运行状态不变，日志中打印相关信息：


#### 日志说明

进行服务化性能数据采集过程中会有日志打印，提示采集进程的状态，可以通过PROF_LOG_LEVEL环境变量控制日志打印。详细操作如下：

PROF_LOG_LEVEL环境变量用于配置数据采集打印日志等级，示例如下：

```
export PROF_LOG_LEVEL=INFO
```

日志等级可设置为（不设置默认等级为INFO）：

- INFO：包含是否开启Profiling数据采集，数据落盘路径等信息。示例如下：
```
1
2
3
```

```
[msservice_profiler] [PID:52856] [INFO] [ReadEnable:306] profile enable_: true
[msservice_profiler] [PID:52856] [INFO] [ReadAclTaskTime:335] profile enableAclTaskTime_: false
[msservice_profiler] [PID:52856] [INFO] [StartProfiler:661] prof path: ./log/0423-0852/

```
|  |  |
| --- | --- |

- DEBUG：详细日志信息，在INFO日志的基础上包含配置文件路径信息，是否开启NPU、CPU数据采集等。示例如下：
```
1
2
3
4
```

```
[msservice_profiler] [PID:82231] [DEBUG] [ReadConfig:275] SERVICE_PROF_CONFIG_PATH : prof.json
[msservice_profiler] [PID:82231] [DEBUG] [ReadLevel:386] profiler_level: 20
[msservice_profiler] [PID:82231] [DEBUG] [ReadHostConfig:510] host_system_usage_freq Disabled
[msservice_profiler] [PID:82231] [DEBUG] [ReadNpuConfig:541] npu_memory_usage_freq Disabled

```
|  |  |
| --- | --- |

- WARNING：除INFO外包含参数配置错误，动态库加载失败等告警信息。
```
1
2
3
4
```

```
[msservice_profiler] [PID:43982] [WARNING] [ReadEnable:323] enable value is not an integer, will set false.
[msservice_profiler] [PID:43984] [WARNING] [ReadEnable:323] enable value is not an integer, will set false.
[msservice_profiler] [PID:43993] [WARNING] [ReadEnable:323] enable value is not an integer, will set false.
[msservice_profiler] [PID:44002] [WARNING] [ReadEnable:323] enable value is not an integer, will set false.

```
|  |  |
| --- | --- |

- ERROR：除报错外无打印日志。示例如下：
```
1
```

```
[msservice_profiler] [PID:87888] [ERROR] [StartProfiler:677] create path(./log/0423-1007/) failed

```
|  |  |
| --- | --- |

**父主题：**[数据采集](atlasprofiling_16_0029.html)