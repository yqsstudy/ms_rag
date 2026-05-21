---
title: "msptiActivityKind"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0259.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0259.html"
---

# msptiActivityKind

[msptiActivityKind为msptiActivityEnable](atlasprofiling_16_0246.html#ZH-CN_TOPIC_0000002504358470)[和msptiActivityDisable](atlasprofiling_16_0247.html#ZH-CN_TOPIC_0000002536038423)调用的枚举类。

MSPTI通过msptiActivityKind对所有能采集到的Activity数据进行分类，每个枚举值对应一个Activity数据的结构体类型。定义如下：

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
```

```
typedef enum {
	MSPTI_ACTIVITY_KIND_INVALID = 0,   // 非法值
	MSPTI_ACTIVITY_KIND_MARKER = 1,   // MSPTI打点能力（标记瞬时时刻）的Activity Record类型，支持最大打点个数为uint32_t最大值，调用结构体msptiActivityMarker
	MSPTI_ACTIVITY_KIND_KERNEL = 2,   // aclnn场景下，计算类算子信息采集的Activity Record类型，调用结构体msptiActivityKernel
	MSPTI_ACTIVITY_KIND_API = 3,   // aclnn场景下，aclnn组件信息采集Activity Record类型，调用结构体msptiActivityApi
	MSPTI_ACTIVITY_KIND_HCCL = 4,   // HCCL通信算子采集Activity Record类型，调用结构体msptiActivityHccl
	MSPTI_ACTIVITY_KIND_MEMORY,   // 内存请求（分配或释放），调用结构体msptiActivityMemory
	MSPTI_ACTIVITY_KIND_MEMSET,   // 内存设置，调用结构体msptiActivityMemset
	MSPTI_ACTIVITY_KIND_MEMCPY,   // 内存拷贝，调用结构体msptiActivityMemcpy
	MSPTI_ACTIVITY_KIND_EXTERNAL_CORRELATION,   // 不同编程API之间的关联记录，调用结构体msptiActivityExternalCorrelation
	MSPTI_ACTIVITY_KIND_COMMUNICATION,   // HCCL和LCCL通信算子采集Activity Record类型，调用结构体msptiActivityCommunication
	MSPTI_ACTIVITY_KIND_COUNT,
	MSPTI_ACTIVITY_KIND_FORCE_INT = 0x7fffffff
} msptiActivityKind;

```
|  |  |
| --- | --- |
**父主题：**[Enumeration类型](atlasprofiling_16_0258.html)