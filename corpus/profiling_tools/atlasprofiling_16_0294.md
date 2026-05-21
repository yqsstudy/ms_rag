---
title: "msptiCallbackIdHccl"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0294.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0294.html"
---

# msptiCallbackIdHccl

[msptiCallbackIdHccl为msptiEnableCallback](atlasprofiling_16_0284.html#ZH-CN_TOPIC_0000002536158469)调用的枚举类。通信API函数的索引的简要定义，在整个API中是唯一的。定义如下：

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
typedef enum {
	MSPTI_CBID_HCCL_INVALID = 0,
	MSPTI_CBID_HCCL_ALLREDUCE = 1,
	MSPTI_CBID_HCCL_BROADCAST = 2,
	MSPTI_CBID_HCCL_ALLGATHER = 3,
	MSPTI_CBID_HCCL_REDUCE_SCATTER = 4,
	MSPTI_CBID_HCCL_REDUCE = 5,
	MSPTI_CBID_HCCL_ALL_TO_ALL = 6,
	MSPTI_CBID_HCCL_ALL_TO_ALLV = 7,
	MSPTI_CBID_HCCL_BARRIER = 8,
	MSPTI_CBID_HCCL_SCATTER = 9,
	MSPTI_CBID_HCCL_SEND = 10,
	MSPTI_CBID_HCCL_RECV = 11,
	MSPTI_CBID_HCCL_SENDRECV = 12,
	MSPTI_CBID_HCCL_SIZE,
	MSPTI_CBID_HCCL_FORCE_INT = 0x7fffffff
} msptiCallbackIdHccl;

```
|  |  |
| --- | --- |
**父主题：**[Enumeration类型](atlasprofiling_16_0290.html)