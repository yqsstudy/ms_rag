---
title: "使用TensorFlow框架接口采集性能数据"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0124.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0124.html"
---

# 使用TensorFlow框架接口采集性能数据

#### 功能介绍

对于TensorFlow训练或在线推理场景，用户可以直接在训练脚本中调用TensorFlow框架相关接口开启性能数据采集，主要包括以下用法：

- 全局采集：采集图执行所有行为的性能数据，数据量比较庞大。
[用户可以通过修改训练脚本、配置“profiling_mode”参数的方式开启（本节重点介绍），也可以通过设置环境变量“PROFILING_MODE”的方式开启（参见使用环境变量采集性能数据](atlasprofiling_16_0139.html#ZH-CN_TOPIC_0000002536038361)），其中配置参数“profiling_mode”的优先级高于环境变量“PROFILING_MODE”。

- 局部采集：支持指定采集局部子图或者指定step的性能数据。通过with语句调用Profiler类，并将需要开启性能数据采集的操作放入Profiler类作用域内的方式实现。

[本节将介绍最基础的全局采集性能数据的方法，了解更多信息，请参见《TensorFlow 1.15模型迁移指南](https://www.hiascend.com/document/detail/zh/TensorFlowCommercial/850/migration/tfmigr1/tfmigr1_000001.html)[》和《TensorFlow 2.6.5模型迁移指南](https://www.hiascend.com/document/detail/zh/TensorFlowCommercial/850/migration/tfmigr2/tfmigr2_000001.html)》。

#### 前提条件

在开启性能采集之前，请确保训练或在线推理脚本可正常执行。

#### 操作步骤

1. 在训练脚本中配置如下信息，以TensorFlow 1.15手工迁移脚本为例：

  - Estimator模式下，您可以尝试先开启task_trace任务轨迹数据采集，代码示例如下：
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
```

```
from npu_bridge.npu_init import *

# enable_profiling：是否开启Profiling采集
# output：Profiling数据存放路径，该参数指定的目录需要在启动训练的环境上（容器或Host侧）提前创建且确保安装时配置的运行用户具有读写权限，支持配置绝对路径或相对路径
# task_trace：是否采集任务轨迹数据
profiling_options = '{"output":"/home/HwHiAiUser/output","task_trace":"on"}'
profiling_config = ProfilingConfig(enable_profiling=True, profiling_options= profiling_options)
session_config=tf.ConfigProto()

config = NPURunConfig(profiling_config=profiling_config, session_config=session_config)

```
|  |  |
| --- | --- |

后续如果仍然无法分析到具体问题，可再开启training_trace迭代轨迹数据采集，代码示例如下：

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
from npu_bridge.npu_init import *

# enable_profiling：是否开启Profiling采集
# output：Profiling数据存放路径
# task_trace：是否采集任务轨迹数据
# training_trace：是否采集迭代轨迹数据
# fp_point：指定训练网络迭代轨迹正向算子的开始位置，用于记录前向计算开始时间戳
# bp_point：指定训练网络迭代轨迹反向算子的结束位置，记录后向计算结束时间戳，fp_point和bp_point可以计算出正反向时间
profiling_options = '{"output":"/home/HwHiAiUser/output","task_trace":"on","training_trace":"on","aicpu":"on","fp_point":"","bp_point":"","aic_metrics":"PipeUtilization"}'
profiling_config = ProfilingConfig(enable_profiling=True, profiling_options= profiling_options)
session_config=tf.ConfigProto(allow_soft_placement=True)

config = NPURunConfig(profiling_config=profiling_config, session_config=session_config)

```
|  |  |
| --- | --- |

  - sess.run模式下，您可以尝试先开启task_trace任务轨迹数据采集，代码示例如下：
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
```

```
custom_op =  config.graph_options.rewrite_options.custom_optimizers.add()
custom_op.name =  "NpuOptimizer"
custom_op.parameter_map["use_off_line"].b = True
custom_op.parameter_map["profiling_mode"].b = True
custom_op.parameter_map["profiling_options"].s = tf.compat.as_bytes('{"output":"/home/HwHiAiUser/output","task_trace":"on"}')
config.graph_options.rewrite_options.remapping = RewriterConfig.OFF
config.graph_options.rewrite_options.memory_optimization = RewriterConfig.OFF

with tf.Session(config=config) as sess:
  sess.run()

```
|  |  |
| --- | --- |

后续如果仍然无法分析到具体问题，可再开启training_trace迭代轨迹数据采集，代码示例如下：

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
```

```
custom_op =  config.graph_options.rewrite_options.custom_optimizers.add()
custom_op.name =  "NpuOptimizer"
custom_op.parameter_map["use_off_line"].b = True
custom_op.parameter_map["profiling_mode"].b = True
custom_op.parameter_map["profiling_options"].s = tf.compat.as_bytes('{"output":"/home/HwHiAiUser/output","task_trace":"on","training_trace":"on","aicpu":"on","fp_point":"","bp_point":"","aic_metrics":"PipeUtilization"}')
config.graph_options.rewrite_options.remapping = RewriterConfig.OFF
config.graph_options.rewrite_options.memory_optimization = RewriterConfig.OFF

with tf.Session(config=config) as sess:
  sess.run()

```
|  |  |
| --- | --- |


  - [Profiling配置的详细介绍请参见Profiling options参数解释](atlasprofiling_16_0301.html#ZH-CN_TOPIC_0000002504198662)。
  - **在Estimator模式下配置enable_profiling****为true****或在sess.run****模式下配置profiling_mode****为true****的情况下。若未配置profiling_options****，Profiling默认会执行t****raining_trace****、task_trace****、hccl****、aicpu****和aic_metrics**（PipeUtilization）采集并保存数据在当前AI任务所在目录。
  - 配置fp_point和bp_point参数时，无论是用户指定了具体算子还是使用系统自动查找算法（fp_point和bp_point参数配置为空），均可能找不到数据，最终导致解析出的迭代轨迹数据中FP_BP、Grad_refresh Bound、Data_aug Bound均为空。

2. 重新执行训练脚本。

*训练结束后，在output参数指定的目录下生成PROF_*XXX文件夹用于存放采集到的原始性能数据。

3. [使用msprof命令解析性能数据。详细请参见离线解析](atlasprofiling_16_0015.html#ZH-CN_TOPIC_0000002536038287)。
********
```
msprof --export=on --output=/home/HwHiAiUser/profiling_output/PROF_XXX
```

解析完成后，在PROF_XXX文件夹下生成mindstudio_profiler_output目录，用户可直接查看。

开启各采集参数后，对应生成的结果文件请参见采集结果说明。

#### 采集结果说明
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