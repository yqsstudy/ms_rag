---
title: "ascend_pytorch_profiler_{Rank_ID}.db数据"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0206.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0206.html"
---

# ascend_pytorch_profiler_{Rank_ID}.db数据

该文件为表结构文件，该文件推荐使用MindStudio Insight工具查看，也可以使用Navicat Premium等数据库开发工具直接打开。当前db文件汇总的性能数据如下：

#### STRING_IDS

映射表，用于存储ID和字符串映射关系。

无开关，记录CANN侧使用的String ID映射关系，通常从0开始累加。
**表1**格式
字段名

类型

索引

含义

id

INTEGER

主键

string对应的id

value

TEXT

-

string内容
|  |  |  |  |
| --- | --- | --- | --- |
|  |  |  |  |
|  |  |  |  |

#### PYTORCH_API

框架侧API数据，当前仅包含torch_npu API数据。

由Ascend PyTorch Profiler接口的torch_npu.profiler.ProfilerActivity.CPU开关控制。
**表2**格式
字段名

类型

含义

startNs

INTEGER

op API开始时间，单位ns

endNs

INTEGER

op API结束时间，单位ns

globalTid

INTEGER

该API所属的全局tid。高32位：pid，低32位：tid

connectionId

INTEGER

用于在CONNECTION_IDS表查询对应的connectionId；如果无connectionId，此处为空

name

INTEGER

该op API名，STRING_IDS(name)

sequenceNumber

INTEGER

op序号

fwdThreadId

INTEGER

op前向线程id

inputDtypes

INTEGER

输入数据类型，STRING_IDS(inputDtypes)

inputShapes

INTEGER

输入shape，STRING_IDS(inputShapes)

callchainId

INTEGER

用于在PYTORCH_CALLCHAINS表查询对应的call stack信息；如果无stack信息，此处为空

type

INTEGER

标记数据类型，op、queue、mstx还是python_trace，数据类型存于枚举表ENUM_API_TYPE中
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

#### CONNECTION_IDS

框架侧API和自身或者和CANN API的关联关系数据。

由Ascend PyTorch Profiler接口的torch_npu.profiler.ProfilerActivity.CPU开关控制。
**表3**格式
字段名

类型

含义

id

INTEGER

对应PYTORCH_API表的connectionId

connectionId

INTEGER

用于表示关联关系的ID，当前包括task_queue、fwd_bwd、torch-cann-task三种关联关系
|  |  |  |
| --- | --- | --- |
|  |  |  |
|  |  |  |

#### PYTORCH_CALLCHAINS

框架侧的堆栈信息。

由Ascend PyTorch Profiler接口的with_stack参数控制。
**表4**格式
字段名

类型

含义

id

INTEGER

对应PYTORCH_API表的callchainId

stack

INTEGER

当前栈的字符串内容在STRING_IDS表中对应的id

stackDepth

INTEGER

当前栈所在深度
|  |  |  |
| --- | --- | --- |
|  |  |  |
|  |  |  |
|  |  |  |

#### MEMORY_RECORD

框架侧的显存占用记录。

由Ascend PyTorch Profiler接口的profile_memory参数控制。
**表5**格式
字段名

类型

含义

component

INTEGER

组件名（GE、PTA、PTA+GE）在STRING_IDS表中对应的id

timestamp

INTEGER

时间戳

totalAllocated

INTEGER

内存分配总额

totalReserved

INTEGER

内存预留总额

totalActive

INTEGER

PTA流申请的总内存

streamPtr

INTEGER

ascendcl流地址

deviceId

INTEGER

设备ID
|  |  |  |
| --- | --- | --- |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |

#### OP_MEMORY

框架侧基于MEMORY_RECORD整合的算子内存占用信息。

由Ascend PyTorch Profiler接口的profile_memory参数控制。
**表6**格式
字段名

类型

含义

name

INTEGER

torch和GE算子名称，STRING_IDS(name)

size

INTEGER

算子占用内存大小，单位Byte

allocationTime

INTEGER

算子内存申请时间，单位ns

releaseTime

INTEGER

算子内存释放时间，单位ns

activeReleaseTime

INTEGER

内存实际归还内存池时间，单位ns

duration

INTEGER

内存占用时间，单位ns

activeDuration

INTEGER

内存实际占用时间，单位ns

allocationTotalAllocated

INTEGER

算子内存分配时PTA和GE内存分配总额，单位Byte

allocationTotalReserved

INTEGER

算子内存分配时PTA和GE内存占用总额，单位Byte

allocationTotalActive

INTEGER

算子内存分配时当前流申请的内存总额，单位Byte

releaseTotalAllocated

INTEGER

算子内存释放时PTA和GE内存分配总额，单位Byte

releaseTotalReserved

INTEGER

算子内存释放时PTA和GE内存占用总额，单位Byte

releaseTotalActive

INTEGER

算子内存释放时当前流申请的内存总额，单位Byte

streamPtr

INTEGER

ascendcl流地址

deviceId

INTEGER

设备ID
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
|  |  |  |
|  |  |  |

#### RANK_DEVICE_MAP

rankId和deviceId的映射关系数据。

无对应开关，导出ascend_pytorch_profiler_{Rank_ID}.db文件时默认生成。
**表7**格式
字段名

类型

含义

rankId

INTEGER

集群场景的节点标识ID，显示为-1时表示未设置rankId。

deviceId

INTEGER

节点上的设备ID，显示为-1时表示未采集到deviceId。
|  |  |  |
| --- | --- | --- |
|  |  |  |
|  |  |  |

#### STEP_TIME

保存Profiler采集step起始时间。

由Ascend PyTorch Profiler接口torch_npu.profiler.schedule类的参数控制。
**表8**格式
字段名

类型

含义

id

INTEGER

Step ID值

startNs

INTEGER

Step开始时间，单位ns

endNs

INTEGER

Step结束时间，单位ns
|  |  |  |
| --- | --- | --- |
|  |  |  |
|  |  |  |
|  |  |  |

#### GC_RECORD

保存Profiler采集的GC事件。

由Ascend PyTorch Profiler接口的gc_detect_threshold参数控制。
**表9**格式
字段名

类型

含义

startNs

INTEGER

GC事件开始时间，单位ns

endNs

INTEGER

GC事件结束时间，单位ns

globalTid

INTEGER

GC事件的全局tid
|  |  |  |
| --- | --- | --- |
|  |  |  |
|  |  |  |
|  |  |  |

#### ROCE

RoCE通信接口带宽数据。

控制开关：

- msprof命令的--sys-io-profiling、--sys-io-sampling-freq
- Ascend PyTorch Profiler的sys_io
- MindSpore Profiler的sys_io
**表10**格式
字段名

类型

含义

deviceId

INTEGER

设备ID

timestampNs

INTEGER

本地时间，单位ns

bandwidth

INTEGER

带宽，单位Byte/s

rxPacketRate

NUMERIC

收包速率，单位packet/s

rxByteRate

NUMERIC

接收字节速率，单位Byte/s

rxPackets

INTEGER

累计收包数量，单位packet

rxBytes

INTEGER

累计接收字节数量，单位Byte

rxErrors

INTEGER

累计接收错误包数量，单位packet

rxDropped

INTEGER

累计接收丢包数量，单位packet

txPacketRate

NUMERIC

发包速率，单位packet/s

txByteRate

NUMERIC

发送字节速率，单位Byte/s

txPackets

INTEGER

累计发包数量，单位packet

txBytes

INTEGER

累计发送字节数量，单位Byte

txErrors

INTEGER

累计发送错误包数量，单位packet

txDropped

INTEGER

累计发送丢包数量，单位packet

funcId

INTEGER

端口号
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
|  |  |  |
|  |  |  |
|  |  |  |

#### NIC

每个时间节点网络信息数据。

控制开关：

- msprof命令的--sys-io-profiling、--sys-io-sampling-freq
- Ascend PyTorch Profiler的sys_io
- MindSpore Profiler的sys_io
**表11**格式
字段名

类型

含义

deviceId

INTEGER

设备ID

timestampNs

INTEGER

本地时间，单位ns

bandwidth

INTEGER

带宽，单位Byte/s

rxPacketRate

NUMERIC

收包速率，单位packet/s

rxByteRate

NUMERIC

接收字节速率，单位Byte/s

rxPackets

INTEGER

累计收包数量，单位packet

rxBytes

INTEGER

累计接收字节数量，单位Byte

rxErrors

INTEGER

累计接收错误包数量，单位packet

rxDropped

INTEGER

累计接收丢包数量，单位packet

txPacketRate

NUMERIC

发包速率，单位packet/s

txByteRate

NUMERIC

发送字节速率，单位Byte/s

txPackets

INTEGER

累计发包数量，单位packet

txBytes

INTEGER

累计发送字节数量，单位Byte

txErrors

INTEGER

累计发送错误包数量，单位packet

txDropped

INTEGER

累计发送丢包数量，单位packet

funcId

INTEGER

端口号
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
|  |  |  |
|  |  |  |
|  |  |  |

#### HCCS

HCCS集合通信带宽数据。

控制开关：

- msprof命令的--sys-interconnection-profiling、--sys-interconnection-freq
- Ascend PyTorch Profiler的sys_interconnection
- MindSpore Profiler的sys_interconnection
**表12**格式
字段名

类型

含义

deviceId

INTEGER

设备ID

timestampNs

INTEGER

本地时间，单位ns

txThroughput

NUMERIC

发送带宽，单位Byte/s

rxThroughput

NUMERIC

接收带宽，单位Byte/s
|  |  |  |
| --- | --- | --- |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |

#### PCIE

PCIe带宽数据。

控制开关：

- msprof命令的--sys-interconnection-profiling、--sys-interconnection-freq
- Ascend PyTorch Profiler的sys_interconnection
- MindSpore Profiler的sys_interconnection
**表13**格式
字段名

类型

含义

deviceId

INTEGER

设备ID

timestampNs

INTEGER

本地时间，单位ns

txPostMin

NUMERIC

发送端PCIe Post数据传输带宽最小值，单位Byte/s

txPostMax

NUMERIC

发送端PCIe Post数据传输带宽最大值，单位Byte/s

txPostAvg

NUMERIC

发送端PCIe Post数据传输带宽平均值，单位Byte/s

txNonpostMin

NUMERIC

发送端PCIe Non-Post数据传输带宽最小值，单位Byte/s

txNonpostMax

NUMERIC

发送端PCIe Non-Post数据传输带宽最大值，单位Byte/s

txNonpostAvg

NUMERIC

发送端PCIe Non-Post数据传输带宽平均值，单位Byte/s

txCplMin

NUMERIC

发送端接收写请求的完成数据包最小值，单位Byte/s

txCplMax

NUMERIC

发送端接收写请求的完成数据包最大值，单位Byte/s

txCplAvg

NUMERIC

发送端接收写请求的完成数据包平均值，单位Byte/s

txNonpostLatencyMin

NUMERIC

发送端PCIe Non-Post模式下的传输时延最小值，单位ns

txNonpostLatencyMax

NUMERIC

发送端PCIe Non-Post模式下的传输时延最大值，单位ns

txNonpostLatencyAvg

NUMERIC

发送端PCIe Non-Post模式下的传输时延平均值，单位ns

rxPostMin

NUMERIC

接收端PCIe Post数据传输带宽最小值，单位Byte/s

rxPostMax

NUMERIC

接收端PCIe Post数据传输带宽最大值，单位Byte/s

rxPostAvg

NUMERIC

接收端PCIe Post数据传输带宽平均值，单位Byte/s。

rxNonpostMin

NUMERIC

接收端PCIe Non-Post数据传输带宽最小值，单位Byte/s

rxNonpostMax

NUMERIC

接收端PCIe Non-Post数据传输带宽最大值，单位Byte/s

rxNonpostAvg

NUMERIC

接收端PCIe Non-Post数据传输带宽平均值，单位Byte/s

rxCplMin

NUMERIC

接收端收到写请求的完成数据包最小值，单位Byte/s

rxCplMax

NUMERIC

接收端收到写请求的完成数据包最大值，单位Byte/s

rxCplAvg

NUMERIC

接收端收到写请求的完成数据包平均值，单位Byte/s
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