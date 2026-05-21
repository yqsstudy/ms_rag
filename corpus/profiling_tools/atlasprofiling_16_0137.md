---
title: "使用Ascend Graph接口采集性能数据"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0137.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0137.html"
---

# 使用Ascend Graph接口采集性能数据

Ascend Graph API是在构图过程中采集性能数据。

#### 支持的型号

Atlas 推理系列产品

Atlas 训练系列产品

Atlas A2 训练系列产品/Atlas A2 推理系列产品

Atlas A3 训练系列产品/Atlas A3 推理系列产品

#### 使能方式介绍
**表1**Profiling性能数据采集方式
方式

接口

GEInitialize接口传入option参数

- ge.exec.profilingMode
- ge.exec.profilingOptions

通过GEInitialize传入option参数ge.exec.profilingOptions，可以采集迭代轨迹数据，传入字段包括training_trace/bp_point/fp_point。

该方式采集的性能数据将存放在ge.exec.profilingOptions的output参数所配置的路径下。

aclgrph接口

- aclgrphProfInit
- aclgrphProfFinalize
- aclgrphProfCreateConfig
- aclgrphProfDestroyConfig
- aclgrphProfStart
- aclgrphProfStop

该方式采集的性能数据将存放在aclgrphProfInit的profiler_path参数所配置的路径下。

注：

[接口详细说明，请参见“GEInitialize](https://www.hiascend.com/document/detail/zh/canncommercial/850/API/ascendgraphapi/atlasgeapi_07_0086.html)[”和“aclgrph API](https://www.hiascend.com/document/detail/zh/canncommercial/850/API/ascendgraphapi/atlasgeapi_07_0077.html)”。
|  |  |
| --- | --- |
|  |  |
|  |  |
|  |  |

#### 采集性能原始数据（GEInitialize接口传入option）

参考以下示例通过GEInitialize传入option参数：
********
```
// 0. System init
std::map<AscendString, AscendString> config = {{"ge.exec.deviceId", "0"},
                        {"ge.graphRunMode", "1"},
                        {"ge.exec.precision_mode", "allow_fp32_to_fp16"},
                        {"ge.exec.profilingMode", "1"},
                        {"ge.exec.profilingOptions",  R"({"output":"/tmp/profiling","training_trace":"on","fp_point":"","bp_point":""})"}};
    Status ret = ge::GEInitialize(config);
    if (ret != SUCCESS) {
        return FAILED;
    }
```

#### 采集性能原始数据（aclgrph接口）

参考以下示例调用接口，采集Profiling性能数据：
****************************
```
  // 构造Graph，该步骤省略
  // ......

  // init ge
  std::map<std::string, std::string> ge_options = {{"ge.socVersion", "Ascendxxx"}, {"ge.graphRunMode", "1"}};
  ge::GEInitialize(ge_options);

  std::string profilerResultPath = "/home/test/prof";       //该路径需要提前创建
  uint32_t length = strlen("/home/test/prof");
  ret = ge::aclgrphProfInit(profilerResultPath.c_str(), length);     

  std::map<string, string> options = {{"a", "b"}, {"c", "d"}};
  uint32_t graphId = 0;

  ge::Session *session = new Session(options);
  ret = session->AddGraph(graphId, graph);

  uint32_t deviceid_list[1] = {0};
  uint32_t device_nums = 1;
  uint64_t data_type_config = ProfDataTypeConfig::kProfTaskTime | ProfDataTypeConfig::kProfAiCoreMetrics | ProfDataTypeConfig::kProfAicpu | ProfDataTypeConfig::kProfTrainingTrace;
  ProfAicoreEvents *aicore_events = NULL;
  ProfilingAicoreMetrics aicore_metrics = ProfilingAicoreMetrics::kAicoreArithmeticUtilization;  
  ge::aclgrphProfConfig *pro_config = ge::aclgrphProfCreateConfig(deviceid_list, device_nums, aicore_metrics, aicore_events, data_type_config);

  ge::aclgrphProfStart(pro_config);

  session->RunGraph(graphId, inputs_r, outputs_r);

  ge::aclgrphProfStop(pro_config);

  ge::aclgrphProfDestroyConfig(pro_config);

  ge::aclgrphProfFinalize();

  delete session;
  ge::GEFinalize();
```

#### 采集数据说明

[配置Ascend Graph API方式采集后请参见离线解析](atlasprofiling_16_0015.html#ZH-CN_TOPIC_0000002536038287)将原始数据文件解析并导出为可视化的timeline和summary文件。生成的Profiling数据如下表所示。
**表2**性能数据文件介绍（GEInitialize接口传入option）
参数

性能数据文件

默认自动生成

[msprof（timeline数据总表）](atlasprofiling_16_0143.html#ZH-CN_TOPIC_0000002536038363)

[msprof_*.json中的Ascend Hardware层级](atlasprofiling_16_0146.html#ZH-CN_TOPIC_0000002504358418)

[step_trace（迭代轨迹数据）](atlasprofiling_16_0148.html#ZH-CN_TOPIC_0000002536158395)

[fusion_op_*.csv](atlasprofiling_16_0158.html#ZH-CN_TOPIC_0000002504358424)

task_time、task_trace

[msprof_*.json中的CANN层级和api_statistic_*.csv文件](atlasprofiling_16_0147.html#ZH-CN_TOPIC_0000002536038365)

[task_time_*.csv](atlasprofiling_16_0146.html#ZH-CN_TOPIC_0000002504358418)

[msprof_*.json中的Communication层级和communication_statistic_*.csv文件](atlasprofiling_16_0150.html#ZH-CN_TOPIC_0000002504358420)

[op_summary_*.csv](atlasprofiling_16_0151.html#ZH-CN_TOPIC_0000002536038367)

[op_statistic_*.csv](atlasprofiling_16_0152.html#ZH-CN_TOPIC_0000002536158397)

runtime_api

[msprof_*.json中的CANN_Runtime层级和api_statistic_*.csv文件](atlasprofiling_16_0147.html#ZH-CN_TOPIC_0000002536038365)

hccl

[msprof_*.json中的Communication层级和communication_statistic_*.csv文件](atlasprofiling_16_0150.html#ZH-CN_TOPIC_0000002504358420)

[api_statistic_*.csv](atlasprofiling_16_0147.html#ZH-CN_TOPIC_0000002536038365)

aicpu

[aicpu_*.csv](atlasprofiling_16_0155.html#ZH-CN_TOPIC_0000002536038369)

host_sys_usage

[Host侧系统CPU利用率数据](atlasprofiling_16_0195.html#ZH-CN_TOPIC_0000002536038397)

[Host侧进程CPU利用率数据](atlasprofiling_16_0196.html#ZH-CN_TOPIC_0000002536158425)

[Host侧系统内存利用率数据](atlasprofiling_16_0197.html#ZH-CN_TOPIC_0000002504198610)

[Host侧进程内存利用率数据](atlasprofiling_16_0198.html#ZH-CN_TOPIC_0000002504358446)
|  |  |
| --- | --- |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
**表3**性能数据文件介绍（aclgrph接口）
参数

性能数据文件

kProfTaskTime

[msprof_*.json中的CANN层级和api_statistic_*.csv文件](atlasprofiling_16_0147.html#ZH-CN_TOPIC_0000002536038365)

[msprof_*.json中的Ascend Hardware层级和task_time_*.csv文件](atlasprofiling_16_0146.html#ZH-CN_TOPIC_0000002504358418)

[msprof_*.json中的Communication层级和communication_statistic_*.csv文件](atlasprofiling_16_0150.html#ZH-CN_TOPIC_0000002504358420)

[op_summary_*.csv](atlasprofiling_16_0151.html#ZH-CN_TOPIC_0000002536038367)

[op_statistic_*.csv](atlasprofiling_16_0152.html#ZH-CN_TOPIC_0000002536158397)

[step_trace（迭代轨迹数据）](atlasprofiling_16_0148.html#ZH-CN_TOPIC_0000002536158395)

[fusion_op_*.csv](atlasprofiling_16_0158.html#ZH-CN_TOPIC_0000002504358424)

kProfHccl

[msprof_*.json中的Communication层级和communication_statistic_*.csv文件](atlasprofiling_16_0150.html#ZH-CN_TOPIC_0000002504358420)

[api_statistic_*.csv](atlasprofiling_16_0147.html#ZH-CN_TOPIC_0000002536038365)

kProfAicpu

[aicpu_*.csv](atlasprofiling_16_0155.html#ZH-CN_TOPIC_0000002536038369)

kProfL2cache

[l2_cache_*.csv](atlasprofiling_16_0157.html#ZH-CN_TOPIC_0000002504198588)

默认自动生成

[Host侧系统CPU利用率数据](atlasprofiling_16_0195.html#ZH-CN_TOPIC_0000002536038397)

[Host侧进程CPU利用率数据](atlasprofiling_16_0196.html#ZH-CN_TOPIC_0000002536158425)

[Host侧系统内存利用率数据](atlasprofiling_16_0197.html#ZH-CN_TOPIC_0000002504198610)

[Host侧进程内存利用率数据](atlasprofiling_16_0198.html#ZH-CN_TOPIC_0000002504358446)
|  |  |
| --- | --- |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
**父主题：**[性能数据其他采集方式](atlasprofiling_16_0123.html)