---
title: "msptiActivityMemory"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0273.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0273.html"
---

# msptiActivityMemory

[msptiActivityMemory为Activity Record类型MSPTI_ACTIVITY_KIND_MEMORY](atlasprofiling_16_0259.html#ZH-CN_TOPIC_0000002536038429)对应的结构体，用于上报Memory Activity信息，定义如下：

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
typedef struct PACKED_ALIGNMENT {
	msptiActivityKind kind;    // Activity Record类型MSPTI_ACTIVITY_KIND_MEMORY
	msptiActivityMemoryOperationType memoryOperationType;    // 用户请求（分配或释放）内存操作
	msptiActivityMemoryKind memoryKind;    // 请求的内存类型
	uint64_t correlationId;    // 内存请求操作的关联ID。每个内存请求操作都被分配一个唯一的关联ID
	uint64_t start;    // 内存请求操作的开始时间戳，单位ns
	uint64_t end;    // 内存请求操作的结束时间戳，单位ns
	uint64_t address;    // 请求的内存地址
	uint64_t bytes;    // 内存请求操作申请的内存字节数
	uint32_t processId;    // 内存请求操作所属的进程ID
	uint32_t deviceId;    // 内存请求操作所在的设备ID
	uint32_t streamId;    // 内存请求操作的流ID，若内存请求操作为异步，则流ID设置为MSPTI_INVALID_STREAM_ID
} msptiActivityMemory;

```
|  |  |
| --- | --- |
**父主题：**[Data Structure类型](atlasprofiling_16_0267.html)