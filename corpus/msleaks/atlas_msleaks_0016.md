---
title: "输出说明"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/msleaks/atlas_msleaks_0016.html"
date_collected: "2026-05-04"
category: "msleaks"
original_path: "zh/mindstudio/830/T&ITools/msleaks/atlas_msleaks_0016.html"
---

# 输出说明

msLeaks工具进行内存分析后，输出的文件如表1。
**表1**输出文件说明
输出文件名称

说明

*leaks_dump_{timestamp*}.csv

使用Step内内存分析功能时，输出内存信息结果文件，并默认保存在“leaksDumpResults/dump”目录下，具体详情信息可参见leaks_dump_{timestamp}.csv文件说明。

*{device**}_**trace_{timestamp*}.json

使用Step内内存分析功能时，输出可视化内存信息结果文件，并默认保存在“leaksDumpResults/trace”目录下，具体详情信息可参见{device}_trace_{timestamp}.json文件说明。
说明：
在MindStudio下一个版本中，将不再落盘json文件，结果通过屏幕打印。

*memory_compare_{timestam*p}.csv

使用内存对比功能时，输出内存对比信息结果文件，记录的是基线内存信息、对比内存信息和对比后的内存差异信息，输出文件默认保存在“leaksDumpResults/compare”目录下，具体详情信息可参见memory_compare_{timestamp}.csv文件说明。

*leaks_dump_{timestamp*}.db

[db格式的内存信息结果文件，可使用MindStudio Insight工具展示，展示结果及具体操作请参见《MindStudio Insight工具用户指南》中的“内存调优](https://www.hiascend.com/document/detail/zh/mindstudio/830/GUI_baseddevelopmenttool/msascendinsightug/Insight_userguide_0120.html)”章节。

*python_trace_{TID**}_{timestamp*}.csv

Python Trace采集的结果文件，默认保存在“leaksDumpResults/dump”目录下，具体详情信息可参见python_trace_{TID}_{timestamp}.csv文件说明。
|  |  |
| --- | --- |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |

#### *leaks_dump_{timestamp*}.csv文件说明
内存泄漏检测的结果文件字段解释如表2所示。**表2***leaks_dump_{timestamp*}.csv文件字段及含义
字段

说明

ID

事件ID。

Event

msLeaks记录的事件类型，包括以下几种类型：

- SYSTEM：系统级事件
- MALLOC：内存申请
- FREE：内存释放
- ACCESS：内存访问
- OP_LAUNCH：算子执行
- KERNEL_LAUNCH：kernel执行
- MSTX：打点

Event Type

事件子类型。

- 当Event为SYSTEM时，Event Type包含ACL_INIT和ACL_FINI。
- 当Event为MALLOC或FREE时，Event Type包含HAL、PTA、MindSpore、ATB、HOST和PTA_WORKSPACE。
- 当Event为ACCESS时，Event Type包含READ、WRITE和UNKNOWN。
- 当Event为OP_LAUNCH时，Event Type包含ATEN_START、ATEN_END、ATB_START和ATB_END。
- 当Event为KERNEL_LAUNCH时，Event Type包含KERNEL_LAUNCH、KERNEL_START和KERNEL_END。
- 当Event为MSTX时，Event Type包含Mark、Range_start和Range_end。

Name

与Event值有关，当Event值为以下值时，Name代表不同的含义。当Event值为其余值时，Name的值为N/A。

- ACCESS：Name为引发访问的算子名/ID。
- OP_LAUNCH：Name为算子名称。
- KERNEL_LAUNCH：Name为kernel名称。
- MSTX：Name为自定义打点名称。

Timestamp(ns)

事件发生的时间。

Process ID

进程号。

Thread ID

线程号。

Device ID

设备信息。

Ptr

内存地址，可以作为标识内存块的id值，一个内存块的生命周期是同一个ptr的malloc到下一次free。

Attr

事件特有属性，每个事件类型有各自的属性项。具体展示信息如下所示：

- 当Event为MALLOC或FREE时，会展示以下参数信息：
  - allocation_id：相同的allocation_id属于对同一块内存的操作。
  - addr：地址。
  - size：本次申请或者释放的内存大小。
  - owner：内存块所有者，多级分类时格式为{A}@{B}@{C}.....，仅当Event为MALLOC时，存在此参数。
  - total：内存池总大小，仅当Event Type为PTA、MindSpore或ATB时，存在此参数。
  - used：内存池总计二次分配大小，仅当Event Type为PTA、MindSpore或ATB时，存在此参数。
  - inefficient：表示是否为低效内存，值表示低效类别，其中early_allocation表示过早申请，late_deallocation表示过迟释放，temporary_idleness表示临时闲置。仅当Event为MALLOC，Event Type为PTA或ATB时，存在此参数。

- 当Event为ACCESS时，会展示以下参数信息：
  - dtype：Tensor的dtype。
  - shape：Tensor的shape。
  - size：Tensor的size。
  - format：Tensor的format。
  - type：访问内存池类型，例如ATB。
  - allocation_id：相同的allocation_id属于对同一块内存的操作，仅当Event Type为PTA时，存在此参数。

- 当Event为OP_LAUNCH，Event Type为ATB_START或ATB_END时，会展示以下参数信息：
  - path：算子在模型中的位置，例如“0_1967120/0/0_GraphOperation/0_ElewiseOperation”，其中包含pid、所属模块名和算子名。
  - workspace ptr：workspace内存起始地址。
  - workspace size：workspace内存大小。

- 当Event为KERNEL_LAUNCH时，会展示以下参数信息：
  - path：kernel在模型中的位置，例如“0_1967120/1/0_GraphOperation/1_ElewiseOperation/0_AddF16Kernel/before”，其中包含pid、所属算子和kernel名，仅当Event Type为KERNEL_START或KERNEL_END时，存在此参数。
  - streamId：stream编号。
  - taskId：任务编号。

Call Stack(Python)

Python调用栈信息（可选）。

Call Stack(C)

C调用栈信息（可选）。
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

#### *{device**}_**trace_{timestamp*}.json文件说明

*可视化内存信息输出文件包含两种json文件，分别为cpu_**trace_{timestamp**}.json（Host侧可视化文件）和npu{id}_**trace_{timestamp**}.json（device侧可视化文件），其中id**代表的是device id，例如npu0_*trace_{timestamp}.json。

[文件可通过Chrome trace（chrome://tracing/）或Perfetto（Perfetto UI](https://ui.perfetto.dev/)）等可视化工具展示，如图1所示。
**图1**
**Host侧可视化信息
图2**
Device侧可视化信息
Host侧和Device侧可视化信息详情如表3，可视化文件和mstx打点信息可以辅助进行内存问题定位和问题代码行确定。**表3**可视化信息详解
文件

名称

说明

*cpu_**trace_{timestamp*}.json（Host侧可视化文件）

Process PID

Kernel Launch打点信息。名称中的PID代表的是进程号。

memory size

cpu上内存信息。当开启Host侧内存采集功能后，会采集到该参数。

pin memory size

hal侧申请的host锁页内存。

*npu{id}_**trace_{timestamp*}.json（device侧可视化文件）

Process PID

Kernel Launch打点信息。名称中的PID代表的是进程号。

*{Framework Name*} allocated memory size

对应框架的内存池allocated信息。

*{Framework Name*} reserved memory size

对应框架的内存池reserved信息。

Thread TID

各Step的持续时间。名称中的TID代表的是线程号。

mstx 0

mstx打点信息。

Thread 0

长时间未释放Step间的内存信息。
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

#### *memory_compare_{timestamp*}.csv文件说明

内存对比的结果文件字段解释如表4所示。
**表4***memory_compare_{timestamp*}.csv文件字段说明
字段

说明

Event

msLeaks记录的对比事件类型，包括OP_LAUNCH和KERNEL_LAUNCH两种类型。

Name

kernel的名称。

Device ID

设备类型、卡号。

Base

input输入的第一个文件路径中的数据。

Compare

input输入的第二个文件路径中的数据。

Allocated Memory(byte)

kernel调用前后的内存变化。

如果为N/A，表示该kernel未被调用。

Diff Memory(byte)

Base和Compare的内存相对变化。

- 当数值为0时，表示该kernel调用所引起的内存变化没有差异。
- 当数值不为0时，表示该kernel调用所引起的内存变化存在差异。
|  |  |
| --- | --- |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |

#### *python_trace_{TID**}_{timestamp*}.csv文件说明
Python Trace采集结果文件的字段解释如表5所示。**表5***python_trace_{TID**}_{timestamp*}.csv文件字段说明
字段

说明

FuncInfo

函数名。

StartTime(ns)

*开始时间戳，和leaks_dump_{timestamp*}.csv中的事件时间戳是一致的。

EndTime(ns)

结束时间戳。

Thread ID

线程ID。

Process ID

进程ID。
|  |  |
| --- | --- |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |