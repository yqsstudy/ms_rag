---
title: "MSPTI工具使用（Python API）"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0022.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0022.html"
---

# MSPTI工具使用（Python API）

#### MSPTI工具Python API介绍

当前提供如下类型的API：

- HcclMonitor：通信算子性能数据采集接口。
- KernelMonitor：Kernel算子性能数据采集接口。
- MstxMonitor：mstx性能数据采集接口。

#### 前提条件

- [请确保完成使用前准备](atlasprofiling_16_0002.html#ZH-CN_TOPIC_0000002504358330)。
- 设置如下环境变量：
```
export LD_PRELOAD=${INSTALL_DIR}/cann/lib64/libmspti.so
```

${INSTALL_DIR}请替换为CANN软件安装后文件存储路径。以root用户安装为例，则安装后文件存储路径为：/usr/local/Ascend/cann。

#### 使用示例

[以下示例仅为MSPTI接口的使用样例，具体可运行样例工程见MSPTI样例集](atlasprofiling_16_0024.html#ZH-CN_TOPIC_0000002536158323)。

[以下接口详细介绍请参见MSPTI Python API参考](atlasprofiling_16_0212.html#ZH-CN_TOPIC_0000002536158433)。

- HcclMonitor
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
from mspti import (
    HcclData,
    HcclMonitor
)

def HcclParser(data : HcclData):
    print(f"[Hccl Info] kind:{data.kind}, start:{data.start}, end:{data.end}, device_id:{data.device_id}, stream_id:{data.stream_id}, bandwidth:{data.bandwidth}, name:{data.name}, comm_name:{data.comm_name}")

monitor = HcclMonitor()
monitor.start(HcclParser)
# 用户业务逻辑
…
monitor.stop()

```
|  |  |
| --- | --- |

- KernelMonitor
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
from mspti import (
    KernelData,
    KernelMonitor
)

def KernelParser(data: KernelData):
    print(f"[Kernel Info] kernel name:{data.name}, start:{data.start}, end:{data.end}, deviceId:{data.device_id}, streamId:{data.stream_id}, type:{data.type}, correlationId:{data.correlation_id}")

monitor = KernelMonitor()
monitor.start(KernelParser)
…
# 业务逻辑
monitor.stop()

```
|  |  |
| --- | --- |

- MstxMonitor
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
14
15
16
17
```

```
from mspti import (
    MarkerData,
    MstxMonitor,
    RangeMarkerData			
)

def MarkerParser(data: MarkerData):
    print(f" [Mark Data Info] flag:{data.flag}, source_kind:{data.source_kind}, timestamp:{data.timestamp}, device_id:{data.object_id.device_id}, stream_id:{ data.object_id.stream_id}, process_id:{data.object_id.process_id}, thread_id:{data.object_id.thread_id}" )

def RangeParser(data: RangeMarkerData):
	print(f"[RangeMark Data Info] kind:{data.kind}, source_kind:{data.source_kind}, id:{data.id}, name:{data.name}, device_id:{data.object_id.device_id}, stream_id:{data.object_id.stream_id}, process_id:{data.object_id.process_id}, thread_id:{data.object_id.thread_id}, start:{data.start}, end:{data.end}")

monitor = MstxMonitor()
monitor.start(MarkerParser,RangeParser)
…
# 业务逻辑
monitor.stop()

```
|  |  |
| --- | --- |

**父主题：**[MSPTI调优工具](atlasprofiling_16_0020.html)