---
title: "创建采集配置文件"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0030.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0030.html"
---

# 创建采集配置文件

服务化性能数据采集通过json配置文件，配置采集数据的开关、保存路径等。

- [自动创建：该文件支持自动创建，在执行采集](atlasprofiling_16_0031.html#ZH-CN_TOPIC_0000002536038299)过程中配置SERVICE_PROF_CONFIG_PATH环境变量后，运行MindIE Motor服务可自动创建默认配置的json文件。
- 手动创建：该json配置文件可以在任意路径下新建，此处以ms_service_profiler_config.json文件名为例，配置文件格式如下：
```
 1
 2
 3
 4
 5
 6
 7
 8
 9
10
11
12
13
```

```
{
    "enable": 1,
    "prof_dir": "${PATH}",
    "profiler_level": "INFO",
    "acl_task_time": 0,
    "acl_prof_task_time_level": "",
    "aclDataTypeConfig": "",
    "aclprofAicoreMetrics": "",
    "api_filter": "",
    "kernel_filter": "",
    "timelimit": 0,
    "domain": ""
}

```
|  |  |
| --- | --- |

**表1**参数说明
参数

说明

是否必选

enable

是否开启性能数据采集的开关，取值为：

- 0：关闭。
- 1：开启。

是

prof_dir

采集到的性能数据的存放路径，可自定义，str类型，默认值为${HOME}/.ms_server_profiler。

否

profiler_level

数据采集等级，取值为INFO。

否

host_system_usage_freq

CPU和内存系统指标采集频率，默认关闭不采集。范围整数1~50，单位Hz，表示每秒采集的次数。设置为-1时关闭采集该指标。
说明：
开启该功能可能占用较大内存，不建议修改。

否

npu_memory_usage_freq

NPU Memory使用率指标的采集频率，默认关闭不采集。范围整数1~50，单位Hz，表示每秒采集的次数。设置为-1时关闭采集该指标。
说明：
开启该功能可能占用较大内存，不建议修改。

否

acl_task_time

开启采集算子下发耗时、算子执行耗时数据的开关，取值为：

- 0：关闭。默认值，配置为0或其他非法值均表示关闭。
- 1：开启。
该功能开启时调用aclprofCreateConfig接口的ACL_PROF_TASK_TIME_L0参数。

- 2：开启基于MSPTI接口的数据落盘。该功能开启时调用MSPTI接口进行性能数据采集，需要在拉起服务前配置如下环境变量：
```
export LD_PRELOAD=${INSTALL_DIR}/lib64/libmspti.so
```

${INSTALL_DIR}请替换为CANN软件安装后文件存储路径。若安装的Ascend-cann-toolkit软件包，以root安装举例，则安装后文件存储路径为：/usr/local/Ascend/ascend-toolkit/latest。

说明：
- [以上aclprofCreateConfig接口及MSPTI接口详细介绍请参见《性能调优工具用户指南](https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0001.html)》。
- 该功能开启时会占用一定的设备性能，导致采集的性能数据不准确，建议在模型执行耗时异常时开启，用于更细致的分析。

否

acl_prof_task_time_level

设置性能数据采集的Level等级和时长，取值为：

- L0：Level0等级，表示采集算子下发耗时、算子执行耗时数据。与L1相比，由于不采集算子基本信息数据，采集时性能开销较小，可更精准统计相关耗时数据。等同于aclDataTypeConfig参数配置ACL_PROF_MSPROFTX、ACL_PROF_TASK_TIME_L0。
- L1：Level1等级，采集AscendCL接口的性能数据，包括Host与Device之间、Device间的同步异步内存复制时延；采集算子下发耗时、算子执行耗时数据以及算子基本信息数据，提供更全面的性能分析数据。等同于aclDataTypeConfig参数配置ACL_PROF_MSPROFTX、ACL_PROF_TASK_TIME、ACL_PROF_ACL_API。
- <time>：采集时长，取值范围为1~999的正整数，单位s。

默认未配置本参数，表示采集L0数据，且采集到程序执行结束。配置其他非法值时取默认值。

采集的Level等级和时长可同时配置，例如"acl_prof_task_time_level": "L1;10"。

否

aclDataTypeConfig

用户选择如下多个宏进行逻辑或，每个宏表示某一类性能数据，取值为：

[以下采集项的结果数据可参见采集数据说明](atlasprofiling_16_0130.html#ZH-CN_TOPIC_0000002504358410)，但具体采集结果请以实际情况为准。

以下采集项一次可以配置一个或多个，例如："aclDataTypeConfig": "ACL_PROF_ACL_API"或"aclDataTypeConfig": "ACL_PROF_ACL_API, ACL_PROF_TASK_TIME"。

- ACL_PROF_ACL_API：表示采集接口的性能数据，包括Host与Device之间、Device间的同步异步内存复制时延等。
- ACL_PROF_TASK_TIME：采集算子下发耗时、算子执行耗时数据以及算子基本信息数据，提供更全面的性能分析数据。
- ACL_PROF_TASK_TIME_L0：采集算子下发耗时、算子执行耗时数据。与ACL_PROF_TASK_TIME相比，由于不采集算子基本信息数据，采集时性能开销较小，可更精准统计相关耗时数据。
- ACL_PROF_OP_ATTR：控制采集算子的属性信息，当前仅支持aclnn算子。
- ACL_PROF_AICORE_METRICS：表示采集AI Core性能指标数据，逻辑或时必须包括该宏，aicoreMetrics入参处配置的性能指标采集项才有效。
- ACL_PROF_TASK_MEMORY：控制CANN算子的内存占用情况采集开关，用于优化内存使用。单算子场景下，按照GE组件维度和算子维度采集算子内存大小及生命周期信息（单算子API执行方式不采集GE组件内存）；静态图和静态子图场景下，在算子编译阶段按照算子维度采集算子内存大小及生命周期信息。
- ACL_PROF_AICPU：表示采集AI CPU任务的开始、结束数据。
- ACL_PROF_L2CACHE：表示采集L2 Cache数据。
- ACL_PROF_HCCL_TRACE：控制通信数据采集开关。
- ACL_PROF_TRAINING_TRACE：控制迭代轨迹数据采集开关。
- ACL_PROF_RUNTIME_API：控制runtime api性能数据采集开关。
- ACL_PROF_MSPROFTX：获取用户和上层框架程序输出的性能数据。可在采集进程内（aclprofStart接口、aclprofStop接口之间）调用如下两种接口开启记录应用程序执行期间特定事件发生的时间跨度，并写入性能数据文件，再使用msprof工具解析该文件，并导出展示性能分析数据：
  - [mstx API（MindStudio Tools Extension API）接口详细操作请参见mstx API使用示例](atlasprofiling_16_0300.html#ZH-CN_TOPIC_0000002536158477)。
  - [msproftx扩展接口详细操作请参见“Profiling性能数据采集](https://www.hiascend.com/document/detail/zh/canncommercial/850/appdevg/acldevg/aclcppdevg_000089.html)”。

默认未配置本参数，以acl_prof_task_time_level参数配置为L0为准。

否

aclprofAicoreMetrics

AI Core性能指标采集项，取值为：

[以下采集项的结果数据可参见op_summary（算子详细信息）](atlasprofiling_16_0151.html#ZH-CN_TOPIC_0000002536038367)，但具体采集结果请以实际情况为准。

以下采集项一次只能配置一个，例如："aclprofAicoreMetrics": "ACL_AICORE_PIPE_UTILIZATION"。

- ACL_AICORE_PIPE_UTILIZATION：计算单元和搬运单元耗时占比。
- ACL_AICORE_MEMORY_BANDWIDTH：外部内存读写类指令占比。
- ACL_AICORE_L0B_AND_WIDTH：内部内存读写类指令占比。
- ACL_AICORE_RESOURCE_CONFLICT_RATIO：流水线队列类指令占比。
- ACL_AICORE_MEMORY_UB：内部内存读写指令占比。
- ACL_AICORE_L2_CACHE：读写cache命中次数和缺失后重新分配次数。
- ACL_AICORE_NONE = 0xFF

默认值为ACL_AICORE_PIPE_UTILIZATION。

仅当aclDataTypeConfig配置了ACL_PROF_AICORE_METRICS后，本接口的配置才能生效。

否

api_filter

对性能数据进行过滤，配置该参数可自定义采集配置的API性能数据，例如传入“matmul”会落盘所有API数据中name字段包含matmul的性能数据。str类型，区分大小写，多个不同的筛选目标用“；”隔开，默认为空，表示落盘所有数据。

仅当acl_task_time参数值为2时生效。

否

kernel_filter

对性能数据进行过滤，配置该参数可自定义采集配置的Kernel性能数据，例如传入“matmul”会落盘所有Kernel数据中name字段包含matmul的性能数据。str类型，区分大小写，多个不同的筛选目标用“；”隔开，默认为空，表示落盘所有数据。

仅当acl_task_time参数值为2时生效。

否

timelimit

设置服务化性能数据采集的时长，配置该参数后，采集进程将在运行指定的时间后自动停止，取值范围为0~7200的整数，单位s，默认值0（表示不限制采集时间）。
说明：
该采集时长建议最短设置为120s，可以根据实际情况进行增加，若采集时间过短，可能会导致数据不满足解析输出件生成，打印告警提示。

否

domain

设置采集指定domain域下的性能数据，减少采集数据量。输入参数为字符串格式，英文分号作为分隔符，区分大小写，例如："Request; KVCache"。

默认为空，表示采集当前所有domain域内性能数据。

当前已有domain域为：Request、KVCache、ModelExecute、BatchSchedule、Communication、eplb_observe。

其中配置eplb_observe域并且使能MindIE专家热点信息采集的接口MINDIE_ENABLE_EXPERT_HOTPOT_GATHER和MINDIE_EXPERT_HOTPOT_DUMP_PATH时，采集到的数据中将包含专家热点信息，解析结果生成专家热点信息热力图。建议用户在需要采集专家热点信息时，单独使能eplb_observe domain域。
说明：
[若指定domain域不全，采集数据不满足解析输出件生成时，则打印告警提示。查看表1](atlasprofiling_16_0035.html#ZH-CN_TOPIC_0000002536038301__zh-cn_topic_0000002502747432_table1985410131831)。

否
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
|  |  |  |
|  |  |  |
**父主题：**[数据采集](atlasprofiling_16_0029.html)