---
title: "KernelData"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0233.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0233.html"
---

# KernelData

[KernelData为KernelMonitor.start](atlasprofiling_16_0220.html#ZH-CN_TOPIC_0000002536158437)调用的结构体，定义如下：

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
class KernelData:
	self.kind   # Activity Record类型MSPTI_ACTIVITY_KIND_KERNEL
	self.start   # Kernel在NPU设备上执行开始时间戳，单位ns。开始和结束时间戳均为0时则无法收集Kernel的时间戳信息
	self.end   # Kernel执行的结束时间戳，单位ns。开始和结束时间戳均为0时则无法收集Kernel的时间戳信息
	self.device_id   # Kernel运行设备的Device ID
	self.stream_id   # Kernel运行流的Stream ID
	self.correlation_id   # Runtime在launch Kernel时生成的唯一ID，其他Activity可通过该值与Kernel进行关联
	self.type    # Kernel的类型
	self.name   # Kernel的名称，该名称在整个Activity Record中保持一致，不建议修改

```
|  |  |
| --- | --- |
**父主题：**[Data Structure类型](atlasprofiling_16_0231.html)