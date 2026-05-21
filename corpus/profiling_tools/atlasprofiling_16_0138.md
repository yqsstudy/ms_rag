---
title: "使用acl.json配置文件采集性能数据"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0138.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0138.html"
---

# 使用acl.json配置文件采集性能数据

离线推理场景下，用户可以在推理程序中调用acl.json文件，读取性能采集参数，从而自动采集性能原始数据。

[采集性能原始数据成功后，可将采集的原始数据取到装有CANN-Toolkit开发套件包和ops算子包的开发环境上进行性能数据解析，展示性能数据解析结果。解析操作请参见离线解析](atlasprofiling_16_0015.html#ZH-CN_TOPIC_0000002536038287)[，解析结果文件介绍请参见性能数据文件参考](atlasprofiling_16_0140.html#ZH-CN_TOPIC_0000002536158391)。

[本节仅介绍如何在推理程序中使能性能数据采集，推理应用完整开发过程请参见《应用开发指南 (C&C++)](https://www.hiascend.com/document/detail/zh/canncommercial/850/appdevg/acldevg/aclcppdevg_000000.html)》。

#### 前提条件

- 在开启性能数据采集之前，请确保推理程序可正常执行。
- **务必调用aclInit()****和aclFinalize**()完成初始化和去初始化。

#### 操作步骤

参考以下步骤完成acl.json文件配置，并完成应用工程编译和运行：

1. **打开aclInit()**函数所在的推理应用工程代码文件，获取acl.json文件路径。

```
1
2
3
4
5
6
7
8
```

```
// ACL init
const char *aclConfigPath = "../src/acl.json";
aclError ret = aclInit(aclConfigPath);
if (ret != ACL_ERROR_NONE) {
    ERROR_LOG("acl init failed");
    return FAILED;
}
INFO_LOG("acl init success");

```
|  |  |
| --- | --- |

如果aclInit()初始化为空，则需要修改该函数，补充步骤2创建的acl.json文件路径。

2. 在查出的目录下修改acl.json文件（如不存在该文件，则需要新建，建议放在工程编译后的src目录下），添加Profiling相关配置，格式如下所示。

```
1
2
3
4
5
6
```

```
{
"profiler": {
        "switch": "on",
        "output": "output"
        }
}

```
|  |  |
| --- | --- |

对于Atlas A2 训练系列产品/Atlas A2 推理系列产品，表1中的instr_profiling_freq与aicpu、aic_metrics、l2、hccl、task_time、ascendcl、runtime_api互斥，无法同时执行。

对于Atlas A3 训练系列产品/Atlas A3 推理系列产品，表1中的instr_profiling_freq与aicpu、aic_metrics、l2、hccl、task_time、ascendcl、runtime_api互斥，无法同时执行。
**表1**profiler参数说明
参数

描述

支持的型号

性能数据文件

switch

Profiling开关，取值on或off。

on表示开启Profiling，off表示关闭Profiling；如果缺失该参数或参数值不为on，则表示关闭Profiling。

开启Profiling开关后自动采集Runtime等接口和Task Scheduler任务调度信息数据。

Atlas 200I/500 A2 推理产品

Atlas 推理系列产品

Atlas 训练系列产品

Atlas A2 训练系列产品/Atlas A2 推理系列产品

Atlas A3 训练系列产品/Atlas A3 推理系列产品

-

output

Profiling性能数据落盘路径。未配置本参数时，性能数据默认落盘到应用工程可执行文件所在目录。

路径中不能包含特殊字符："\n", "\\n", "\f", "\\f", "\r", "\\r", "\b", "\\b", "\t", "\\t", "\v", "\\v", "\u007F", "\\u007F", "\"", "\\\"", "'", "\'", "\\", "\\\\", "%", "\\%", ">", "\\>", "<", "\\<", "|", "\\|", "&", "\\&", "$", "\\$", ";", "\\;", "`", "\\`"。
Profiling采集结束后，在该目录下生成PROF开头目录，存放Profiling采集的性能原始数据。支持配置绝对路径或相对路径（相对执行命令行时的当前路径）：
  - 绝对路径配置以“/”开头
  - 相对路径配置直接以目录名开始，例如：output。
  - 该参数指定的目录需要确保安装时配置的运行用户具有读写权限。如果该处设置的目录没有读写权限，默认存放采集结果数据到应用工程可执行文件所在目录（确保安装时配置的运行用户具有该目录的读写权限）。
  - [该参数优先级高于ASCEND_WORK_PATH，具体请参考《环境变量参考](https://www.hiascend.com/document/detail/zh/canncommercial/850/maintenref/envvar/envref_07_0001.html)》。

Atlas 200I/500 A2 推理产品

Atlas 推理系列产品

Atlas 训练系列产品

Atlas A2 训练系列产品/Atlas A2 推理系列产品

Atlas A3 训练系列产品/Atlas A3 推理系列产品

-

storage_limit

指定落盘目录允许存放的最大文件容量。当Profiling数据文件在磁盘中即将占满本参数设置的最大存储空间或剩余磁盘总空间即将被占满时（总空间剩余<=20MB），则将磁盘内最早的文件进行老化删除处理。

**范围[200, 4294967295]，单位为MB，例如storage****_limit**=200MB，默认未配置本参数。

未配置本参数时，默认取值为Profiling数据文件存放目录所在磁盘可用空间的90%。

Atlas 200I/500 A2 推理产品

Atlas 推理系列产品

Atlas 训练系列产品

Atlas A2 训练系列产品/Atlas A2 推理系列产品

Atlas A3 训练系列产品/Atlas A3 推理系列产品

-

aicpu

采集AI CPU算子的详细信息，如：算子执行时间、数据拷贝时间等。可选on或off，默认值为off。

Atlas 200I/500 A2 推理产品

Atlas 推理系列产品

Atlas 训练系列产品

Atlas A2 训练系列产品/Atlas A2 推理系列产品

Atlas A3 训练系列产品/Atlas A3 推理系列产品

[aicpu_*.csv](atlasprofiling_16_0155.html#ZH-CN_TOPIC_0000002536038369)

[dp_*.csv](atlasprofiling_16_0149.html#ZH-CN_TOPIC_0000002504198584)

aic_metrics

AI Core和AI Vector Core采集事件。task_time配置为on、l1时，该参数生效；task_time配置为l0或off时，不执行该参数采集。

取值包括：

  - Atlas 200I/500 A2 推理产品：ArithmeticUtilization、PipeUtilization、Memory、MemoryL0、MemoryUB、ResourceConflictRatio、L2Cache、PipelineExecuteUtilization（默认值）
  - Atlas 推理系列产品：ArithmeticUtilization、PipeUtilization（默认值）、Memory、MemoryL0、MemoryUB、ResourceConflictRatio
  - Atlas 训练系列产品：ArithmeticUtilization、PipeUtilization（默认值）、Memory、MemoryL0、MemoryUB、ResourceConflictRatio
  - Atlas A2 训练系列产品/Atlas A2 推理系列产品：ArithmeticUtilization、PipeUtilization（默认值）、Memory、MemoryL0、MemoryUB、ResourceConflictRatio、L2Cache、MemoryAccess
  - Atlas A3 训练系列产品/Atlas A3 推理系列产品：ArithmeticUtilization、PipeUtilization（默认值）、Memory、MemoryL0、MemoryUB、ResourceConflictRatio、L2Cache、MemoryAccess
**说明： 支持自定义需要采集的寄存器，例如："aic_metrics":"Custom:***0x49,0x8,0x15,0x1b,0x64,0x10*"。
  - Custom字段表示自定义类型，配置为具体的寄存器值，范围[0x1, 0x6E]。
  - 配置的寄存器数最多不能超过8个，寄存器通过“,”区分开。
  - 寄存器的值支持十六进制或十进制。

Atlas 200I/500 A2 推理产品：支持AI Core和AI Vector Core采集

Atlas 推理系列产品：支持AI Core采集

Atlas 训练系列产品：支持AI Core采集

Atlas A2 训练系列产品/Atlas A2 推理系列产品：支持AI Core和AI Vector Core采集

Atlas A3 训练系列产品/Atlas A3 推理系列产品：支持AI Core和AI Vector Core采集

[op_summary_*.csv](atlasprofiling_16_0151.html#ZH-CN_TOPIC_0000002536038367)

l2

控制L2 Cache采样数据的开关，可选on或off，默认为off。

  - Atlas 200I/500 A2 推理产品：分析AI Core命中L2次数推荐使用aic-metrics=L2Cache。
  - Atlas A2 训练系列产品/Atlas A2 推理系列产品：分析AI Core命中L2次数推荐使用aic-metrics=L2Cache。
  - Atlas A3 训练系列产品/Atlas A3 推理系列产品：分析AI Core命中L2次数推荐使用aic-metrics=L2Cache。

Atlas 200I/500 A2 推理产品

Atlas 推理系列产品

Atlas 训练系列产品

Atlas A2 训练系列产品/Atlas A2 推理系列产品

Atlas A3 训练系列产品/Atlas A3 推理系列产品

[l2_cache_*.csv](atlasprofiling_16_0157.html#ZH-CN_TOPIC_0000002504198588)

hccl

控制通信数据采集开关。该数据只在多卡、多节点或集群场景下生成。

  - json文件中配置该参数时，可选配on或off。
  - json文件中未配置该参数时，默认为空，不采集；当task_time设置为on时，该参数联动被设置为on。 说明：
此开关后续版本会废弃，请使用task_time开关控制相关数据采集。

Atlas 200I/500 A2 推理产品

Atlas 推理系列产品

Atlas 训练系列产品

Atlas A2 训练系列产品/Atlas A2 推理系列产品

Atlas A3 训练系列产品/Atlas A3 推理系列产品

[msprof_*.json中的Communication层级和communication_statistic_*.csv文件](atlasprofiling_16_0150.html#ZH-CN_TOPIC_0000002504358420)

[api_statistic_*.csv](atlasprofiling_16_0147.html#ZH-CN_TOPIC_0000002536038365)

task_time

控制采集算子下发耗时和算子执行耗时的开关。涉及在task_time、op_summary、op_statistic等文件中输出相关耗时数据。配置值：

  - on：开启。默认为on。
  - off：关闭。
  - l0：采集算子下发耗时、算子执行耗时数据。与l1相比，由于不采集算子基本信息数据，采集时性能开销较小，可更精准统计相关耗时数据。
  - l1：采集算子下发耗时、算子执行耗时数据以及算子基本信息数据，提供更全面的性能分析数据，和配置为on的效果一样。

Atlas 200I/500 A2 推理产品

Atlas 推理系列产品

Atlas 训练系列产品

Atlas A2 训练系列产品/Atlas A2 推理系列产品

Atlas A3 训练系列产品/Atlas A3 推理系列产品

[msprof_*.json中的CANN层级和api_statistic_*.csv文件](atlasprofiling_16_0147.html#ZH-CN_TOPIC_0000002536038365)

[msprof_*.json中的Ascend Hardware层级](atlasprofiling_16_0146.html#ZH-CN_TOPIC_0000002504358418)

[msprof_*.json中的Communication层级和communication_statistic_*.csv文件](atlasprofiling_16_0150.html#ZH-CN_TOPIC_0000002504358420)（该数据只在多卡、多节点或集群场景下生成）

[step_trace（迭代轨迹数据）](atlasprofiling_16_0148.html#ZH-CN_TOPIC_0000002536158395)

[op_summary_*.csv](atlasprofiling_16_0151.html#ZH-CN_TOPIC_0000002536038367)

[op_statistic_*.csv](atlasprofiling_16_0152.html#ZH-CN_TOPIC_0000002536158397)

[fusion_op_*.csv](atlasprofiling_16_0158.html#ZH-CN_TOPIC_0000002504358424)

ascendcl

控制acl接口性能数据采集的开关，可选on或off，默认为on。

可采集acl接口性能数据，包括Host与Device之间、Device间的同步异步内存复制时延等。

Atlas 200I/500 A2 推理产品

Atlas 推理系列产品

Atlas 训练系列产品

Atlas A2 训练系列产品/Atlas A2 推理系列产品

Atlas A3 训练系列产品/Atlas A3 推理系列产品

[msprof_*.json中的CANN_AscendCL层级和api_statistic_*.csv文件](atlasprofiling_16_0147.html#ZH-CN_TOPIC_0000002536038365)

runtime_api

控制runtime API性能数据采集开关，可选on或off，默认为on。

可采集runtime API性能数据，包括Host与Device之间、Device间的同步异步内存复制时延等。

Atlas 200I/500 A2 推理产品

Atlas 推理系列产品

Atlas 训练系列产品

Atlas A2 训练系列产品/Atlas A2 推理系列产品

Atlas A3 训练系列产品/Atlas A3 推理系列产品

[msprof_*.json中的CANN_Runtime层级和api_statistic_*.csv文件](atlasprofiling_16_0147.html#ZH-CN_TOPIC_0000002536038365)

sys_hardware_mem_freq

片上内存、QoS带宽及内存信息采集频率、LLC的读写带宽数据采集频率、Acc PMU数据和SOC传输带宽信息采集频率、组件内存采集频率。

范围[1,100]，单位Hz。

[已知在安装有glibc<2.34的环境上采集memory数据，可能触发glibc的一个已知Bug 19329](https://sourceware.org/bugzilla/show_bug.cgi?id=19329)，通过升级环境的glibc版本可解决此问题。
说明：
对于以下产品，采集任务结束后，不建议用户增大采集频率，否则可能导致SoC传输带宽数据丢失。

Atlas 200I/500 A2 推理产品

Atlas A2 训练系列产品/Atlas A2 推理系列产品

Atlas A3 训练系列产品/Atlas A3 推理系列产品

Atlas 200I/500 A2 推理产品

Atlas 推理系列产品

Atlas 训练系列产品

Atlas A2 训练系列产品/Atlas A2 推理系列产品

Atlas A3 训练系列产品/Atlas A3 推理系列产品

不同产品支持情况不同，请以实际实现为准。

[片上内存读写速率文件](atlasprofiling_16_0168.html#ZH-CN_TOPIC_0000002536158409)

[msprof_*.json中的LLC层级和llc_read_write_*.csv文件](atlasprofiling_16_0178.html#ZH-CN_TOPIC_0000002504358434)

[msprof_*.json中的acc_pmu层级](atlasprofiling_16_0175.html#ZH-CN_TOPIC_0000002536038383)

[msprof_*.json中的Stars Soc Info层级](atlasprofiling_16_0176.html#ZH-CN_TOPIC_0000002536158413)

[msprof_*.json中的NPU MEM层级和npu_mem_*.csv文件](atlasprofiling_16_0159.html#ZH-CN_TOPIC_0000002536038373)

[npu_module_mem_*.csv](atlasprofiling_16_0160.html#ZH-CN_TOPIC_0000002536158405)

llc_profiling

LLC Profiling采集事件，可以设置为：

  - Atlas 200I/500 A2 推理产品：
    - read：读事件，三级缓存读速率。
    - write：写事件，三级缓存写速率。默认为read。

  - Atlas 推理系列产品：
    - read：读事件，三级缓存读速率。
    - write：写事件，三级缓存写速率。默认为read。

  - Atlas 训练系列产品：
    - read：读事件，三级缓存读速率。
    - write：写事件，三级缓存写速率。默认为read。

  - Atlas A2 训练系列产品/Atlas A2 推理系列产品：
    - read：读事件，三级缓存读速率。
    - write：写事件，三级缓存写速率。默认为read。

  - Atlas A3 训练系列产品/Atlas A3 推理系列产品：
    - read：读事件，三级缓存读速率。
    - write：写事件，三级缓存写速率。默认为read。

Atlas 200I/500 A2 推理产品

Atlas 推理系列产品

Atlas 训练系列产品

Atlas A2 训练系列产品/Atlas A2 推理系列产品

Atlas A3 训练系列产品/Atlas A3 推理系列产品

采集该数据需要设置sys_hardware_mem_freq。

sys_io_sampling_freq

NIC、ROCE采集频率。范围[1,100]，单位Hz。

  - Atlas 200I/500 A2 推理产品：仅RC场景支持采集NIC，容器场景参数不生效
  - Atlas 训练系列产品：支持采集NIC和ROCE
  - Atlas A2 训练系列产品/Atlas A2 推理系列产品：支持采集NIC和ROCE
  - Atlas A3 训练系列产品/Atlas A3 推理系列产品：支持采集NIC和ROCE

Atlas 200I/500 A2 推理产品

Atlas 训练系列产品

Atlas A2 训练系列产品/Atlas A2 推理系列产品

Atlas A3 训练系列产品/Atlas A3 推理系列产品

[msprof_*.json中的NIC层级和nic_*.csv文件](atlasprofiling_16_0171.html#ZH-CN_TOPIC_0000002536038381)

[msprof_*.json中的RoCE层级和roce_*.csv文件](atlasprofiling_16_0172.html#ZH-CN_TOPIC_0000002536158411)

sys_interconnection_freq

集合通信带宽数据（HCCS）、SIO数据、PCIe数据采集频率，片间传输带宽信息采集频率。

范围[1,50]，默认值50，单位Hz。

  - Atlas 推理系列产品：支持采集PCIe数据
  - Atlas 训练系列产品：支持采集HCCS、PCIe数据
  - Atlas A2 训练系列产品/Atlas A2 推理系列产品：支持采集HCCS、PCIe数据、片间传输带宽信息
  - Atlas A3 训练系列产品/Atlas A3 推理系列产品：支持采集HCCS、PCIe数据、片间传输带宽信息、SIO数据

Atlas 推理系列产品

Atlas 训练系列产品

Atlas A2 训练系列产品/Atlas A2 推理系列产品

Atlas A3 训练系列产品/Atlas A3 推理系列产品

[msprof_*.json中的PCIe层级和pcie_*.csv文件](atlasprofiling_16_0173.html#ZH-CN_TOPIC_0000002504198596)

[msprof_*.json中的HCCS层级和hccs_*.csv文件](atlasprofiling_16_0170.html#ZH-CN_TOPIC_0000002504358430)

[msprof_*.json中的Stars Chip Trans层级](atlasprofiling_16_0177.html#ZH-CN_TOPIC_0000002504198598)

dvpp_freq

DVPP采集频率。

范围[1,100]，单位Hz。

Atlas 200I/500 A2 推理产品

Atlas 推理系列产品支持采集但暂不支持数据解析

Atlas 训练系列产品

Atlas A2 训练系列产品/Atlas A2 推理系列产品

Atlas A3 训练系列产品/Atlas A3 推理系列产品

Atlas 推理系列产品不支持解析该性能数据

[dvpp_*.csv](atlasprofiling_16_0182.html#ZH-CN_TOPIC_0000002504358436)

instr_profiling_freq

AI Core和AI Vector的带宽和延时采集频率，范围[300,30000]，单位Hz。
说明：
仅单算子场景支持。

Atlas A2 训练系列产品/Atlas A2 推理系列产品

Atlas A3 训练系列产品/Atlas A3 推理系列产品

[msprof_*.json中的biu_group、aic_core_group、aiv_core_group层级](atlasprofiling_16_0174.html#ZH-CN_TOPIC_0000002504358432)

host_sys

Host侧性能数据采集开关，取值包括：

  - cpu：进程级别的CPU利用率。
  - mem：进程级别的内存利用率。

可选其中的一项或多项，选多项时用英文逗号隔开，例如"host_sys": "cpu,mem"。

Atlas 200I/500 A2 推理产品

Atlas 推理系列产品

Atlas 训练系列产品

Atlas A2 训练系列产品/Atlas A2 推理系列产品

Atlas A3 训练系列产品/Atlas A3 推理系列产品

[msprof_*.json中的CPU Usage层级和host_cpu_usage_*.csv文件](atlasprofiling_16_0190.html#ZH-CN_TOPIC_0000002504358442)

[msprof_*.json中的Memory Usage层级和host_mem_usage_*.csv文件](atlasprofiling_16_0191.html#ZH-CN_TOPIC_0000002536038393)

host_sys_usage

采集Host侧系统及所有进程的CPU和内存数据，取值包括cpu和mem。

可选其中的一项或多项，选多项时用英文逗号隔开，例如"host_sys_usage": "cpu,mem"。

Atlas 200I/500 A2 推理产品

Atlas 推理系列产品

Atlas 训练系列产品

Atlas A2 训练系列产品/Atlas A2 推理系列产品

Atlas A3 训练系列产品/Atlas A3 推理系列产品

[Host侧系统CPU利用率数据](atlasprofiling_16_0195.html#ZH-CN_TOPIC_0000002536038397)

[Host侧进程CPU利用率数据](atlasprofiling_16_0196.html#ZH-CN_TOPIC_0000002536158425)

[Host侧系统内存利用率数据](atlasprofiling_16_0197.html#ZH-CN_TOPIC_0000002504198610)

[Host侧进程内存利用率数据](atlasprofiling_16_0198.html#ZH-CN_TOPIC_0000002504358446)

host_sys_usage_freq

配置Host侧系统和所有进程CPU、内存数据的采集频率。

范围[1,50]，默认值50，单位Hz。

Atlas 200I/500 A2 推理产品

Atlas 推理系列产品

Atlas 训练系列产品

Atlas A2 训练系列产品/Atlas A2 推理系列产品

Atlas A3 训练系列产品/Atlas A3 推理系列产品

-

msproftx

控制msproftx用户和上层框架程序输出性能数据的开关，可选on或off，默认值为off。

Profiling开启msproftx功能之前，需要在程序内调用msproftx相关接口来开启程序的Profiling数据流的输出，调用如下两种接口开启记录应用程序执行期间特定事件发生的时间跨度，并写入性能数据文件，再使用msprof工具解析该文件，并导出展示性能分析数据：

  - [mstx API（MindStudio Tools Extension API）接口详细操作请参见mstx API使用示例](atlasprofiling_16_0300.html#ZH-CN_TOPIC_0000002536158477)。
  - [msproftx扩展接口详细操作请参见《应用开发指南 (C&C++)](https://www.hiascend.com/document/detail/zh/canncommercial/850/appdevg/acldevg/aclcppdevg_000000.html)[》中的“Profiling性能数据采集](https://www.hiascend.com/document/detail/zh/canncommercial/850/appdevg/acldevg/aclcppdevg_000089.html)”。

Atlas 200I/500 A2 推理产品

Atlas 推理系列产品

Atlas 训练系列产品

Atlas A2 训练系列产品/Atlas A2 推理系列产品

Atlas A3 训练系列产品/Atlas A3 推理系列产品

[msproftx数据说明](atlasprofiling_16_0145.html#ZH-CN_TOPIC_0000002504198582)
|  |  |  |  |
| --- | --- | --- | --- |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |

3. [配置acl.json文件完成后，参考《应用开发指南 (C&C++)](https://www.hiascend.com/document/detail/zh/canncommercial/850/appdevg/acldevg/aclcppdevg_000000.html)》重新编译应用工程、并运行应用工程。

“output”指定路径下生成Profiling性能原始数据，如图1所示。
**图1**
Profiling性能原始数据
如果acl.json文件之前已经存在，本处仅是修改文件内容、添加Profiling相关配置，则不需要重新编译应用工程。

**父主题：**[性能数据其他采集方式](atlasprofiling_16_0123.html)