---
title: "msptiActivityMemset"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0274.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0274.html"
---

# msptiActivityMemset

[msptiActivityMemset为Activity Record类型MSPTI_ACTIVITY_KIND_MEMSET](atlasprofiling_16_0259.html#ZH-CN_TOPIC_0000002536038429)对应的结构体，用于上报Memset Activity信息，定义如下：

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
	msptiActivityKind kind;    // Activity Record类型MSPTI_ACTIVITY_KIND_MEMSET
	uint32_t value;    // Memset设置的目标值
	uint64_t bytes;    // Memset设置的字节数
	uint64_t start;    //  Memset操作的开始时间戳，单位ns
	uint64_t end;    //  Memset操作的结束时间戳，单位ns
	uint32_t deviceId;    // Memset操作所在的设备ID
	uint32_t streamId;    // Memset操作的流ID
	uint64_t correlationId;    // Memset操作的关联ID
	uint8_t isAsync;    // 是否通过异步内存API进行内存设置操作
} msptiActivityMemset;

```
|  |  |
| --- | --- |
**父主题：**[Data Structure类型](atlasprofiling_16_0267.html)