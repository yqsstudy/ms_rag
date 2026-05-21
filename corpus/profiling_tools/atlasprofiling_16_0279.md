---
title: "msptiObjectId"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0279.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0279.html"
---

# msptiObjectId

[msptiObjectId为msptiActivityMarker](atlasprofiling_16_0272.html#ZH-CN_TOPIC_0000002536158463)调用，用于识别Marker的进程ID、线程ID、Device ID、Stream ID。定义如下：

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
typedef union PACKED_ALIGNMENT {
	struct {
		uint32_t processId;   // ActivityMarker的进程ID
		uint32_t threadId;   // ActivityMarker的线程ID
	} pt;
	struct {
		uint32_t deviceId;   // ActivityMarker进程所在设备的Device ID
		uint32_t streamId;   //  ActivityMarker进程所在流的Stream ID
	} ds;
} msptiObjectId;

```
|  |  |
| --- | --- |
**父主题：**[Union类型](atlasprofiling_16_0278.html)