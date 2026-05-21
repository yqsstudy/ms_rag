---
title: "采集数据说明"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0130.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0130.html"
---

# 采集数据说明

[采集性能数据后请参见离线解析](atlasprofiling_16_0015.html#ZH-CN_TOPIC_0000002536038287)将原始数据文件解析并导出为可视化的性能数据文件，保存在PROF_XXX/mindstudio_profiler_output目录下。

生成的性能数据如表1所示。
**表1**性能数据文件介绍
参数

性能数据文件

ACL_PROF_TASK_TIME

ACL_PROF_TASK_TIME_L0

[msprof_*.json中的CANN层级和api_statistic_*.csv文件](atlasprofiling_16_0147.html#ZH-CN_TOPIC_0000002536038365)

[msprof_*.json中的Ascend Hardware层级和task_time_*.csv文件](atlasprofiling_16_0146.html#ZH-CN_TOPIC_0000002504358418)

[msprof_*.json中的Communication层级和communication_statistic_*.csv文件](atlasprofiling_16_0150.html#ZH-CN_TOPIC_0000002504358420)

[step_trace（迭代轨迹数据）](atlasprofiling_16_0148.html#ZH-CN_TOPIC_0000002536158395)

[op_summary_*.csv](atlasprofiling_16_0151.html#ZH-CN_TOPIC_0000002536038367)

[op_statistic_*.csv](atlasprofiling_16_0152.html#ZH-CN_TOPIC_0000002536158397)

[fusion_op_*.csv](atlasprofiling_16_0158.html#ZH-CN_TOPIC_0000002504358424)

ACL_PROF_ACL_API

[msprof_*.json中的CANN_AscendCL层级和api_statistic_*.csv文件](atlasprofiling_16_0147.html#ZH-CN_TOPIC_0000002536038365)

ACL_PROF_RUNTIME_API

[msprof_*.json中的CANN_Runtime层级和api_statistic_*.csv文件](atlasprofiling_16_0147.html#ZH-CN_TOPIC_0000002536038365)

ACL_PROF_HCCL_TRACE

[msprof_*.json中的Communication层级和communication_statistic_*.csv文件](atlasprofiling_16_0150.html#ZH-CN_TOPIC_0000002504358420)

[api_statistic_*.csv](atlasprofiling_16_0147.html#ZH-CN_TOPIC_0000002536038365)

ACL_PROF_AICPU

[aicpu_*.csv](atlasprofiling_16_0155.html#ZH-CN_TOPIC_0000002536038369)

ACL_PROF_AICORE_METRICS

[op_summary_*.csv](atlasprofiling_16_0151.html#ZH-CN_TOPIC_0000002536038367)

ACL_PROF_L2CACHE

[l2_cache_*.csv](atlasprofiling_16_0157.html#ZH-CN_TOPIC_0000002504198588)

ACL_PROF_TASK_MEMORY

[memory_record_*.csv](atlasprofiling_16_0161.html#ZH-CN_TOPIC_0000002504198590)

[operator_memory_*.csv](atlasprofiling_16_0162.html#ZH-CN_TOPIC_0000002504358426)

[static_op_mem_*.csv](atlasprofiling_16_0163.html#ZH-CN_TOPIC_0000002536038377)

ACL_PROF_MSPROFTX

[msproftx数据](atlasprofiling_16_0145.html#ZH-CN_TOPIC_0000002504198582)

ACL_PROF_SYS_HARDWARE_MEM_FREQ

[片上内存读写速率文件](atlasprofiling_16_0168.html#ZH-CN_TOPIC_0000002536158409)

[msprof_*.json中的LLC层级和llc_read_write_*.csv文件](atlasprofiling_16_0178.html#ZH-CN_TOPIC_0000002504358434)

[msprof_*.json中的acc_pmu层级](atlasprofiling_16_0175.html#ZH-CN_TOPIC_0000002536038383)

[msprof_*.json中的Stars Soc Info层级](atlasprofiling_16_0176.html#ZH-CN_TOPIC_0000002536158413)

[msprof_*.json中的NPU MEM层级和npu_mem_*.csv文件](atlasprofiling_16_0159.html#ZH-CN_TOPIC_0000002536038373)

[npu_module_mem_*.csv](atlasprofiling_16_0160.html#ZH-CN_TOPIC_0000002536158405)

ACL_PROF_SYS_IO_FREQ

[msprof_*.json中的NIC层级和nic_*.csv文件](atlasprofiling_16_0171.html#ZH-CN_TOPIC_0000002536038381)

[msprof_*.json中的RoCE层级和roce_*.csv文件](atlasprofiling_16_0172.html#ZH-CN_TOPIC_0000002536158411)

ACL_PROF_SYS_INTERCONNECTION_FREQ

[msprof_*.json中的PCIe层级和pcie_*.csv文件](atlasprofiling_16_0173.html#ZH-CN_TOPIC_0000002504198596)

[msprof_*.json中的HCCS层级和hccs_*.csv文件](atlasprofiling_16_0170.html#ZH-CN_TOPIC_0000002504358430)

[msprof_*.json中的Stars Chip Trans层级](atlasprofiling_16_0177.html#ZH-CN_TOPIC_0000002504198598)

ACL_PROF_DVPP_FREQ

[dvpp_*.csv](atlasprofiling_16_0182.html#ZH-CN_TOPIC_0000002504358436)

ACL_PROF_HOST_SYS

[msprof_*.json中的CPU Usage层级和host_cpu_usage_*.csv文件](atlasprofiling_16_0190.html#ZH-CN_TOPIC_0000002504358442)

[msprof_*.json中的Memory Usage层级和host_mem_usage_*.csv文件](atlasprofiling_16_0191.html#ZH-CN_TOPIC_0000002536038393)

ACL_PROF_HOST_SYS_USAGE

ACL_PROF_HOST_SYS_USAGE_FREQ

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
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
**父主题：**[使用acl C&C++接口采集性能数据](atlasprofiling_16_0125.html)