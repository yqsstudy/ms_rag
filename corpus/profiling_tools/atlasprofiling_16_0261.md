---
title: "msptiActivitySourceKind"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0261.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0261.html"
---

# msptiActivitySourceKind

标记Activity数据来源。标记数据的来源是Host还是Device。

[msptiActivitySourceKind为msptiActivityMarker](atlasprofiling_16_0272.html#ZH-CN_TOPIC_0000002536158463)结构体内调用的枚举类，定义如下：

```
1
2
3
4
```

```
typedef enum {
	MSPTI_ACTIVITY_SOURCE_KIND_HOST = 0,   // 标记数据的来源是Host
	MSPTI_ACTIVITY_SOURCE_KIND_DEVICE = 1   // 标记数据的来源是Device
} msptiActivitySourceKind;

```
|  |  |
| --- | --- |
**父主题：**[Enumeration类型](atlasprofiling_16_0258.html)