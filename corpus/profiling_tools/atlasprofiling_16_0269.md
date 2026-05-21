---
title: "msptiActivityApi"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0269.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0269.html"
---

# msptiActivityApi

[msptiActivityApi为Activity Record类型MSPTI_ACTIVITY_KIND_API](atlasprofiling_16_0259.html#ZH-CN_TOPIC_0000002536038429)对应的结构体，定义如下：

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
```

```
typedef struct PACKED_ALIGNMENT {
	msptiActivityKind kind;   // Activity Record类型MSPTI_ACTIVITY_KIND_API
	uint64_t start;   // API执行的开始时间戳，单位ns。开始和结束时间戳均为0时则无法收集API的时间戳信息
	uint64_t end;   // API执行的结束时间戳，单位ns。开始和结束时间戳均为0时则无法收集API的时间戳信息
	struct {
		uint32_t processId;   // API运行设备的进程ID
		uint32_t threadId;   // API运行流的线程ID
	} pt;
	uint64_t correlationId;   // API的关联ID。每个API执行都被分配一个唯一的关联ID，该关联ID与启动API的驱动程序或运行时API Activity Record的关联ID相同
	const char* name;   // API的名称，该名称在整个Activity Record中保持一致，不建议修改
} msptiActivityApi;

```
|  |  |
| --- | --- |
**父主题：**[Data Structure类型](atlasprofiling_16_0267.html)