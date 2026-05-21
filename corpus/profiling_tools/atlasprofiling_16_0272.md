---
title: "msptiActivityMarker"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0272.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0272.html"
---

# msptiActivityMarker

[msptiActivityMarker为Activity Record类型MSPTI_ACTIVITY_KIND_MARKER](atlasprofiling_16_0259.html#ZH-CN_TOPIC_0000002536038429)对应的结构体，定义如下：

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
```

```
typedef struct PACKED_ALIGNMENT {
	msptiActivityKind kind;   // Activity Record类型MSPTI_ACTIVITY_KIND_MARKER
	msptiActivityFlag flag;   // 打点的flag标记
	msptiActivitySourceKind sourceKind;   // 标记数据的来源类型
	uint64_t timestamp;   // 标记的时间戳，单位ns。值为0时表示无法为标记收集时间戳信息
	uint64_t id;   // 标记的ID
	msptiObjectId objectId;   // 识别Marker的进程ID、线程ID、Device ID、Stream ID
	const char *name;   // 标记的名称，结束标记时值为NULL
	const char *domain;   // 标记所属domain域的名称，默认域为NULL
} msptiActivityMarker;

```
|  |  |
| --- | --- |
**父主题：**[Data Structure类型](atlasprofiling_16_0267.html)