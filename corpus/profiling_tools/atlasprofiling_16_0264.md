---
title: "msptiActivityMemcpyKind"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0264.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0264.html"
---

# msptiActivityMemcpyKind

内存拷贝类型

[msptiActivityMemcpyKind为msptiActivityMemcpy](atlasprofiling_16_0275.html#ZH-CN_TOPIC_0000002536038437)调用的枚举类，定义如下：

```
1
2
3
4
5
6
7
8
```

```
typedef enum {
	MSPTI_ACTIVITY_MEMCPY_KIND_UNKNOWN = 0,    // 内部预留，未定义
	MSPTI_ACTIVITY_MEMCPY_KIND_HOST = 1,    // Host到Host的内存拷贝类型
	MSPTI_ACTIVITY_MEMCPY_KIND_HTOD = 2,    // Host到Device的内存拷贝类型
	MSPTI_ACTIVITY_MEMCPY_KIND_DTOH = 3,    // Device到Host的内存拷贝类型
	MSPTI_ACTIVITY_MEMCPY_KIND_DTOD = 4,    // Device到Device的内存拷贝类型
	MSPTI_ACTIVITY_MEMCPY_KIND_DEFAULT = 5    // 同一Device上的设备内存到设备内存的拷贝类型
} msptiActivityMemcpyKind;

```
|  |  |
| --- | --- |
**父主题：**[Enumeration类型](atlasprofiling_16_0258.html)