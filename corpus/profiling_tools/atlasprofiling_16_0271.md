---
title: "msptiActivityKernel"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0271.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0271.html"
---

# msptiActivityKernel

[msptiActivityKernel为Activity Record类型MSPTI_ACTIVITY_KIND_KERNEL](atlasprofiling_16_0259.html#ZH-CN_TOPIC_0000002536038429)对应的结构体，定义如下：

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
```

```
typedef struct PACKED_ALIGNMENT {
	msptiActivityKind kind;   // Activity Record类型MSPTI_ACTIVITY_KIND_KERNEL
	uint64_t start;   // Kernel在NPU设备上执行开始时间戳，单位ns。开始和结束时间戳均为0时则无法收集Kernel的时间戳信息
	uint64_t end;   // Kernel执行的结束时间戳，单位ns。开始和结束时间戳均为0时则无法收集Kernel的时间戳信息
	struct {
		uint32_t deviceId;   // Kernel运行设备的Device ID
		uint32_t streamId;   // Kernel运行流的Stream ID
	} ds;
	uint64_t correlationId;   // Runtime在launch Kernel时生成的唯一ID，其他Activity可通过该值与Kernel进行关联
	const char *type;   // Kernel的类型
	const char *name;   // Kernel的名称，该名称在整个Activity Record中保持一致，不建议修改
} msptiActivityKernel;

```
|  |  |
| --- | --- |
**父主题：**[Data Structure类型](atlasprofiling_16_0267.html)