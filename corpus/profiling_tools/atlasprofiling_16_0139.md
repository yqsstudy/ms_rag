---
title: "使用环境变量采集性能数据"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0139.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0139.html"
---

# 使用环境变量采集性能数据

环境变量方式采集适用于TensorFlow框架训练/在线推理场景。与直接使用TensorFlow框架接口采集方式不同的是，环境变量方式是在训练/在线推理脚本中直接插入PROFILING_OPTIONS环境变量配置性能数据采集项。

#### 前提条件

- 训练场景：
  - [准备好基于TensorFlow 1.15开发的训练模型以及配套的数据集，并按照《TensorFlow 1.15模型迁移指南](https://www.hiascend.com/document/detail/zh/TensorFlowCommercial/850/migration/tfmigr1/tfmigr1_000001.html)》完成TensorFlow原始模型向昇腾AI处理器的迁移。
  - [准备好基于TensorFlow 2.x开发的训练模型以及配套的数据集，并按照《TensorFlow 2.6.5模型迁移指南](https://www.hiascend.com/document/detail/zh/TensorFlowCommercial/850/migration/tfmigr2/tfmigr2_000001.html)》完成TensorFlow原始模型向昇腾AI处理器的迁移。

- 在线推理场景：下载预训练模型并准备在线推理脚本。

#### 操作步骤
配置的环境变量内容示例如下。************************************************************
```
export PROFILING_MODE=true
export PROFILING_OPTIONS='{"output":"/tmp/profiling","training_trace":"on","task_trace":"on","fp_point":"","bp_point":"","aic_metrics":"PipeUtilization"}'
```

**PROFILING_OPTIONS**[参数解释及使用方法，请参见Profiling options参数解释](atlasprofiling_16_0301.html#ZH-CN_TOPIC_0000002504198662)。

**配置PROFILING_MODE****为true****但未配置PROFILING_OPTIONS****情况下Profiling默认会执行training_trace****、task_trace****、hccl****、aicpu****和aic_metrics****（PipeUtilization）采集并将采集到的数据保存在当前AI任务所在目录；当配置PROFILING_MODE****为true****且配置PROFILING_OPTIONS****任意参数后，PROFILING_OPTIONS**[参数默认情况请参见Profiling options参数解释](atlasprofiling_16_0301.html#ZH-CN_TOPIC_0000002504198662)。

#### 采集结果说明

[配置PROFILING_OPTIONS参数后请参见离线解析](atlasprofiling_16_0015.html#ZH-CN_TOPIC_0000002536038287)将原始数据文件解析并导出为可视化的性能数据文件，保存在PROF_XXX/mindstudio_profiler_output目录下。

采集的结果文件如表1所示。
**表1**采集结果文件
参数

结果文件

默认自动生成

[msprof（timeline数据总表）](atlasprofiling_16_0143.html#ZH-CN_TOPIC_0000002536038363)

[op_summary_*.csv](atlasprofiling_16_0151.html#ZH-CN_TOPIC_0000002536038367)

[op_statistic_*.csv](atlasprofiling_16_0152.html#ZH-CN_TOPIC_0000002536158397)

[fusion_op_*.csv](atlasprofiling_16_0158.html#ZH-CN_TOPIC_0000002504358424)

[step_trace（迭代轨迹数据）](atlasprofiling_16_0148.html#ZH-CN_TOPIC_0000002536158395)

task_trace、task_time

[msprof_*.json中的CANN层级和api_statistic_*.csv文件](atlasprofiling_16_0147.html#ZH-CN_TOPIC_0000002536038365)

[msprof_*.json中的Ascend Hardware层级和task_time_*.csv文件](atlasprofiling_16_0146.html#ZH-CN_TOPIC_0000002504358418)

[msprof_*.json中的Communication层级和communication_statistic_*.csv文件](atlasprofiling_16_0150.html#ZH-CN_TOPIC_0000002504358420)

[step_trace_*.json](atlasprofiling_16_0148.html#ZH-CN_TOPIC_0000002536158395)

runtime_api

[msprof_*.json中的CANN_Runtime层级和api_statistic_*.csv文件](atlasprofiling_16_0147.html#ZH-CN_TOPIC_0000002536038365)

hccl

[msprof_*.json中的Communication层级和communication_statistic_*.csv文件](atlasprofiling_16_0150.html#ZH-CN_TOPIC_0000002504358420)

[api_statistic_*.csv](atlasprofiling_16_0147.html#ZH-CN_TOPIC_0000002536038365)

aicpu

[aicpu_*.csv](atlasprofiling_16_0155.html#ZH-CN_TOPIC_0000002536038369)

[dp_*.csv](atlasprofiling_16_0149.html#ZH-CN_TOPIC_0000002504198584)

aic_metrics

[op_summary_*.csv](atlasprofiling_16_0151.html#ZH-CN_TOPIC_0000002536038367)

l2

[l2_cache_*.csv](atlasprofiling_16_0157.html#ZH-CN_TOPIC_0000002504198588)

msproftx

[msproftx数据](atlasprofiling_16_0145.html#ZH-CN_TOPIC_0000002504198582)

sys_hardware_mem_freq

[片上内存读写速率文件](atlasprofiling_16_0168.html#ZH-CN_TOPIC_0000002536158409)

[msprof_*.json中的LLC层级和llc_read_write_*.csv文件](atlasprofiling_16_0178.html#ZH-CN_TOPIC_0000002504358434)

[msprof_*.json中的acc_pmu层级](atlasprofiling_16_0175.html#ZH-CN_TOPIC_0000002536038383)

[msprof_*.json中的Stars Soc Info层级](atlasprofiling_16_0176.html#ZH-CN_TOPIC_0000002536158413)

[msprof_*.json中的NPU MEM层级和npu_mem_*.csv文件](atlasprofiling_16_0159.html#ZH-CN_TOPIC_0000002536038373)

[npu_module_mem_*.csv](atlasprofiling_16_0160.html#ZH-CN_TOPIC_0000002536158405)

llc_profiling

-

sys_io_sampling_freq

[msprof_*.json中的NIC层级和nic_*.csv文件](atlasprofiling_16_0171.html#ZH-CN_TOPIC_0000002536038381)

[msprof_*.json中的RoCE层级和roce_*.csv文件](atlasprofiling_16_0172.html#ZH-CN_TOPIC_0000002536158411)

sys_interconnection_freq

[msprof_*.json中的PCIe层级和pcie_*.csv文件](atlasprofiling_16_0173.html#ZH-CN_TOPIC_0000002504198596)

[msprof_*.json中的HCCS层级和hccs_*.csv文件](atlasprofiling_16_0170.html#ZH-CN_TOPIC_0000002504358430)

[msprof_*.json中的Stars Chip Trans层级](atlasprofiling_16_0177.html#ZH-CN_TOPIC_0000002504198598)

dvpp_freq

[dvpp_*.csv](atlasprofiling_16_0182.html#ZH-CN_TOPIC_0000002504358436)

instr_profiling_freq

[msprof_*.json中的biu_group、aic_core_group、aiv_core_group层级](atlasprofiling_16_0174.html#ZH-CN_TOPIC_0000002504358432)

host_sys

[msprof_*.json中的CPU Usage层级和host_cpu_usage_*.csv文件](atlasprofiling_16_0190.html#ZH-CN_TOPIC_0000002504358442)

[msprof_*.json中的Memory Usage层级和host_mem_usage_*.csv文件](atlasprofiling_16_0191.html#ZH-CN_TOPIC_0000002536038393)

host_sys_usage

[Host侧系统CPU利用率数据](atlasprofiling_16_0195.html#ZH-CN_TOPIC_0000002536038397)

[Host侧进程CPU利用率数据](atlasprofiling_16_0196.html#ZH-CN_TOPIC_0000002536158425)

[Host侧系统内存利用率数据](atlasprofiling_16_0197.html#ZH-CN_TOPIC_0000002504198610)

[Host侧进程内存利用率数据](atlasprofiling_16_0198.html#ZH-CN_TOPIC_0000002504358446)

host_sys_usage_freq

-
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
|  |  |
**父主题：**[性能数据其他采集方式](atlasprofiling_16_0123.html)