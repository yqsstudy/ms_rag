---
title: "HcclData"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0232.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0232.html"
---

# HcclData

[HcclData为HcclMonitor.start](atlasprofiling_16_0215.html#ZH-CN_TOPIC_0000002536038407)调用的结构体，定义如下：

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
```

```
class HcclData:
	self.kind   # Activity Record类型MSPTI_ACTIVITY_KIND_HCCL
	self.start   # 通信算子在NPU设备上执行开始时间戳，单位ns。开始和结束时间戳均为0时则无法收集通信算子的时间戳信息
	self.end   # 通信算子执行的结束时间戳，单位ns。开始和结束时间戳均为0时则无法收集通信算子的时间戳信息
	self.device_id   # 通信算子运行设备的Device ID
	self.stream_id   # 通信算子运行流的Stream ID
	self.bandwidth   # 通信算子运行时的带宽，单位GB/s
	self.name   # 通信算子的名称
	self.comm_name   # 通信域的名称

```
|  |  |
| --- | --- |
**父主题：**[Data Structure类型](atlasprofiling_16_0231.html)