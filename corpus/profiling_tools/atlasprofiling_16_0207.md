---
title: "analysis.db数据"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0207.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0207.html"
---

# analysis.db数据

该文件为表结构文件，推荐使用MindStudio Insight工具查看，也可以使用Navicat Premium等数据库开发工具直接打开。当前db文件汇总的性能数据如下：

#### CommAnalyzerBandwidth
**表1**格式
字段名

类型

含义

hccl_op_name

TEXT

通信大算子名，例：hcom_broadcast__303_1_1

group_name

TEXT

通信域hash ID，例：3915571125887837303

transport_type

TEXT

传输类型，包含：LOCAL、SDMA、RDMA

transit_size

NUMERIC

传输的数据量，单位MB

transit_time

NUMERIC

传输耗时，单位ms

bandwidth

NUMERIC

带宽，单位GB/s

large_packet_ratio

NUMERIC

大数据包的比例

package_size

NUMERIC

一次传输的通信数据包大小，单位MB

count

NUMERIC

通信传输次数

total_duration

NUMERIC

数据传输总耗时

step

TEXT

算子所属的step，例：step12

type

TEXT

算子类型，包含：Collective，P2P
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

#### CommAnalyzerTime
**表2**格式
字段名

类型

含义

hccl_op_name

TEXT

通信算子名称。

group_name

TEXT

通信算子的分组。

start_timestamp

NUMERIC

通信开始时间戳，单位us。

elapse_time

NUMERIC

算子的通信总耗时，单位ms。

transit_time

NUMERIC

通信时长，单位ms。表示通信算子的通信耗时，如果通信耗时过长，可能是某条链路存在问题。

wait_time

NUMERIC

等待时长，单位ms。节点之间通信前首先需要进行同步，确保通信的两个节点同步完成，再进行通信。

synchronization_time

NUMERIC

同步时长，单位ms。节点之间进行同步需要的时长。

idle_time

NUMERIC

空闲时间，单位ms。空闲时间（idle_time） = 算子的通信总耗时（elapse_time） - 通信时长（transit_time） - 等待时长（wait_time）。

step

TEXT

算子所属的step

type

TEXT

算子类型，包含：Collective，P2P
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

#### CommAnalyzerMatrix
**表3**格式
字段名

类型

含义

hccl_op_name

TEXT

矩阵分析后的精简算子名，例：send-top1

group_name

TEXT

通信域hash ID，例：3915571125887837303

src_rank

TEXT

发送数据的rankId，例：0

dst_rank

TEXT

接收数据的rankId，例：1

transport_type

TEXT

传输类型，包含：LOCAL、SDMA、RDMA

transit_size

NUMERIC

传输的数据量，单位MB

transit_time

NUMERIC

传输耗时，单位ms

bandwidth

NUMERIC

带宽，单位GB/s

step

TEXT

算子所属的step，例：step12

type

TEXT

算子类型，包含：Collective，P2P

op_name

TEXT

算子的原始名字，例：hcom_broadcast__303_1_1
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

#### StepTraceTime
**表4**格式
字段名

类型

含义

deviceId

INTEGER

设备ID

step

TEXT

step编号，例：12

computing

NUMERIC

计算的时间，单位ms

communication

NUMERIC

通信的时间，单位ms

overlapped

NUMERIC

同时进行计算和通信的时间，单位ms

communication_not_overlapped

NUMERIC

纯用于通信的时间，单位ms

free

NUMERIC

空闲的时间，单位ms

stage

NUMERIC

step内除去接收数据的时间，单位ms

bubble

NUMERIC

step内用于接收数据的时间，单位ms

communication_not_overlapped_and_exclude_receive

NUMERIC

纯用于通信的时间减去用于接收数据的时间，单位ms
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
**父主题：**[MindSpore&PyTorch框架性能数据文件参考](atlasprofiling_16_0203.html)