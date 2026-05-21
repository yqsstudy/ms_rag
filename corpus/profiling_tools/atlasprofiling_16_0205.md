---
title: "timeline和summary数据"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0205.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0205.html"
---

# timeline和summary数据

#### trace_view.json
**图1**
trace_view
如图1所示，trace数据主要展示如下区域：

- 区域1：上层应用数据，包含上层应用算子的耗时信息。
- 区域2：CANN层数据，主要包含AscendCL、GE和Runtime组件的耗时数据。
- 区域3：底层NPU数据，主要包含Task Scheduler组件耗时数据和迭代轨迹数据以及其他昇腾AI处理器系统数据。
- 区域4：展示trace中各算子、接口的详细信息。单击各个trace事件时展示。

trace_view.json支持使用MindStudio Insight工具、chrome://tracing/和https://ui.perfetto.dev/打开。
**图2**
trace_view（record_shapes）
开启record_shapes时，trace_view中的上层应用算子会显示Input Dims和Input type信息。

仅PyTorch场景支持，MindSpore场景暂不支持record_shapes控制此数据。
**图3**
trace_view（with_stack）
开启with_stack时，trace_view中的上层应用算子会显示Call stack信息。
**图4**
trace_view（GC）
图4采集结果中Python GC层的时间段为本次GC执行的时间。

[GC执行时，会阻塞当前进程，需要等待GC完成，若GC时间过长，可以通过调整GC参数（可参考垃圾回收器](https://docs.python.org/zh-cn/3/library/gc.html)中的gc.set_threshold）来缓解GC造成的进程阻塞。

仅PyTorch场景支持。

#### kernel_details.csv
**图5**
**kernel_details（MindSpore）
图6**
kernel_details（PyTorch）
文件包含在NPU上执行的所有算子的信息。若用户前端调用了schedule进行Step打点，则会增加Step Id字段；但若schedule设置了warmup（不为0），且训练/在线推理的每个Step后存在算子异步执行操作，那么这部分算子异步执行操作在warmup阶段执行的算子可能会被采集到，结果为在kernel_details.csv中没有Step Id字段。

字段信息如表1所示。

[当配置experimental_config的aic_metrics参数时，kernel_details.csv文件将根据experimental_config参数的aic_metrics配置增加对应字段，主要增加内容请参见experimental_config参数说明](atlasprofiling_16_0121.html#ZH-CN_TOPIC_0000002504198570__zh-cn_topic_0000002534478481_section1548285513313)[，文件内相关字段详细介绍请参见op_summary（算子详细信息）](atlasprofiling_16_0151.html#ZH-CN_TOPIC_0000002536038367)。
**表1**kernel_details
字段名

字段解释

Step Id&Step ID

迭代ID。

Device_id

设备ID。

Model ID

模型ID。

Task ID

Task任务的ID。

Stream ID

该Task所处的Stream ID。

Name

算子名。

Type

算子类型。

OP State

算子的动静态信息，dynamic表示动态算子，static表示静态算子，通信算子无该状态显示为N/A，该字段仅在--task-time=l1情况下上报，--task-time=l0时显示为N/A。

Accelerator Core

AI加速核类型，包括AI Core、AI CPU等。

Start Time(us)

算子执行开始时间，单位us。

Duration(us)

当前算子执行耗时，单位us。

Wait Time(us)

算子执行等待时间，单位us。

Block Dim

运行切分数量，对应任务执行时核数。

Mix Block Dim

部分算子同时在AI Core和Vector Core上执行，主加速器的Block Dim在Block Dim字段描述，从加速器的Block Dim在本字段描述。task_time为l0时，不采集该字段，显示为N/A。（Atlas A2 训练系列产品/Atlas A2 推理系列产品）（Atlas A3 训练系列产品/Atlas A3 推理系列产品）

HF32 Eligible

标识是否使用HF32精度标记，YES表示使用，NO表示未使用。

Input Shapes

算子输入Shape。

Input Data Types

算子输入数据类型。

Input Formats

算子输入数据格式。

Output Shapes

算子输出Shape。

Output Data Types

算子输出数据类型。

Output Formats

算子输出数据格式。
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
|  |  |
|  |  |
|  |  |
|  |  |

#### memory_record.csv
**图7**
memory_record
文件包含PTA和GE的显存占用记录，主要记录PTA、GE等组件申请的内存及占用时间。字段信息如表2所示。
**表2**memory_record
字段名

字段解释

Component

组件，包含：

- MindSpore：MindSpore、MindSpore+GE组件、APP进程级等。
- PyTorch：PTA和GE组件、APP进程级、WORKSPACE（采集性能数据前配置环境变量TASK_QUEUE_ENABLE=2时生成）等。

Timestamp(us)

时间戳，记录显存占用的起始时间，单位us。

Total Allocated(MB)

内存分配总额，单位MB。

Total Reserved(MB)

内存预留总额，单位MB。

Total Active(MB)

Stream流所申请的总内存（包括被其他流复用的未释放的内存），单位MB。

Stream Ptr

AscendCL流的内存地址，用于标记不同的AscendCL流。

Device Type

设备类型和设备ID，仅涉及NPU。
|  |  |
| --- | --- |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |

#### operator_memory.csv
**图8**
operator_memory
文件包含算子的内存占用明细，主要记录算子在NPU上执行所需内存及占用时间，其中内存由PTA和GE申请。字段信息如表3所示。

[若operator_memory.csv文件中出现负值或空值，详细原因请参见负值空值说明](atlasprofiling_16_0162.html#ZH-CN_TOPIC_0000002504358426__zh-cn_topic_0000002534398415_section73121012154017)。
**表3**operator_memory
字段名

字段解释

Name

算子名称。

Size(KB)

算子占用内存大小，单位KB。

Allocation Time(us)

Tensor内存分配时间，单位us。

Release Time(us)

Tensor内存释放时间，单位us。

Active Release Time(us)

内存实际归还内存池时间，单位us。

Duration(us)

内存占用时间（Release Time-Allocation Time），单位us。

Active Duration(us)

内存实际占用时间（Active Release Time-Allocation Time），单位us。

Allocation Total Allocated(MB)

算子内存分配时的内存分配总额（Name算子名称为aten开头时为PTA内存，算子名称为cann开头时为GE内存），单位MB。

Allocation Total Reserved(MB)

算子内存分配时的内存占用总额（Name算子名称为aten开头时为PTA内存，算子名称为cann开头时为GE内存），单位MB。

Allocation Total Active(MB)

算子内存分配时当前流所申请的总内存（包括被其他流复用的未释放的内存），单位MB。

Release Total Allocated(MB)

算子内存释放时的内存分配总额（Name算子名称为aten开头时为PTA内存，算子名称为cann开头时为GE内存），单位MB。

Release Total Reserved(MB)

算子内存释放时的内存占用总额（Name算子名称为aten开头时为PTA内存，算子名称为cann开头时为GE内存），单位MB。

Release Total Active(MB)

算子内存释放时的内存中被其他Stream复用的内存总额（Name算子名称为aten开头时为PTA内存，算子名称为cann开头时为GE内存），单位MB。

Stream Ptr

AscendCL流的内存地址，用于标记不同的AscendCL流。

Device Type

设备类型和设备ID，仅涉及NPU。
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

#### npu_module_mem.csv
**图9**
**npu_module_mem（MindSpore）
图10**
npu_module_mem（PyTorch）
npu_module_mem.csv数据在采集进程中自动采集，包含组件级的内存占用情况，主要记录组件在NPU上执行时，当前时刻所占用的内存。字段信息如表4所示。
**表4**npu_module_mem
字段名

字段解释

Device_id

设备ID。

Component

组件名称。

Timestamp(us)

时间戳，表示当前时刻组件占用的内存，单位us。

Total Reserved(MB)&Total Reserved(KB)

内存占用大小，单位MB（PyTorch）&KB（MindSpore）。

Device

设备类型和设备ID，仅涉及NPU。
|  |  |
| --- | --- |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |

#### operator_details.csv
**图11**
operator_details
operator_details.csv文件包含信息如表5所示。
**表5**operator_details
字段

说明

Name

算子名称。

Input Shapes

Shape信息。

Call Stack

函数调用栈信息。由with_stack字段控制。

Host Self Duration(us)

算子在Host侧的耗时（除去内部调用的其他算子），单位us。

Host Total Duration(us)

算子在Host侧的耗时，单位us。

Device Self Duration(us)

算子在Device侧的耗时（除去内部调用的其他算子），单位us。

Device Total Duration(us)

算子在Device侧的耗时，单位us。

Device Self Duration With AICore(us)

算子在Device侧执行在AI Core上的耗时（除去内部调用的算子），单位us。

Device Total Duration With AICore(us)

算子在Device侧执行在AI Core上的耗时，单位us。
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

#### step_trace_time.csv
**图12**
**step_trace_time（MindSpore）
图13**
step_trace_time（PyTorch）

迭代中计算和通信的时间统计，包含信息如表6所示。
**表6**step_trace_time
字段

说明

Device_id

设备ID。

Step

迭代数。

Computing

NPU上算子的计算总时间，单位us。

Communication(Not Overlapped)

通信时间，通信总时间减去计算和通信重叠的时间，单位us。

Overlapped

计算和通信重叠的时间，单位us。更多重叠代表计算和通信之间更好的并行性。理想情况下，通信与计算完全重叠。

Communication

NPU上算子的通信总时间，单位us。

Free

迭代总时间减去计算和通信时间，单位us。可能包括初始化、数据加载、CPU计算等。

Stage

Stage时间，代表除receive算子时间外的时间，单位us。

Bubble

指receive时间的总和，单位us。

Communication(Not Overlapped and Exclude Receive)

通信总时间减去计算和通信重叠以及receive算子的时间，单位us。

Preparing

迭代开始到首个计算或通信算子运行的时间，单位us。
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

#### data_preprocess.csv

[data_preprocess.csv文件记录AI CPU数据，示例和字段说明以aicpu（AI CPU算子详细耗时）](atlasprofiling_16_0155.html#ZH-CN_TOPIC_0000002536038369)为参考，实际结果略有不同，请以实际情况为准。

#### l2_cache.csv

[示例和字段说明以l2_cache（L2 Cache命中率）](atlasprofiling_16_0157.html#ZH-CN_TOPIC_0000002504198588)为参考，实际结果略有不同，请以实际情况为准。

#### op_statistic.csv

[示例和字段说明以op_statistic（算子调用次数及耗时）](atlasprofiling_16_0152.html#ZH-CN_TOPIC_0000002536158397)为参考，实际结果略有不同，请以实际情况为准。

#### api_statistic.csv

[示例和字段说明以api_statistic_*.csv文件说明](atlasprofiling_16_0147.html#ZH-CN_TOPIC_0000002536038365__zh-cn_topic_0000002502718410_section11622953115117)为参考，实际结果略有不同，请以实际情况为准。

#### pcie.csv

[示例和字段说明以pcie_*.csv文件说明](atlasprofiling_16_0173.html#ZH-CN_TOPIC_0000002504198596__zh-cn_topic_0000002502718424_section12139135285518)为参考，实际结果略有不同，请以实际情况为准。

#### hccs.csv

[示例和字段说明以hccs_*.csv文件说明](atlasprofiling_16_0170.html#ZH-CN_TOPIC_0000002504358430__zh-cn_topic_0000002534398447_section12139135285518)为参考，实际结果略有不同，请以实际情况为准。

#### nic.csv

[示例和字段说明以nic_*.csv文件说明](atlasprofiling_16_0171.html#ZH-CN_TOPIC_0000002536038381__zh-cn_topic_0000002502558600_section10366164515)为参考，实际结果略有不同，请以实际情况为准。

#### roce.csv

[示例和字段说明以roce_*.csv文件说明](atlasprofiling_16_0172.html#ZH-CN_TOPIC_0000002536158411__zh-cn_topic_0000002534398449_section11791341554)为参考，实际结果略有不同，请以实际情况为准。
**父主题：**[MindSpore&PyTorch框架性能数据文件参考](atlasprofiling_16_0203.html)