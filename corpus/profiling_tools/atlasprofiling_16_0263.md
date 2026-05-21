---
title: "msptiActivityMemoryKind"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0263.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0263.html"
---

# msptiActivityMemoryKind

请求的内存类型。

[msptiActivityMemoryKind为msptiActivityMemory](atlasprofiling_16_0273.html#ZH-CN_TOPIC_0000002504198648)调用的枚举类，定义如下：

```
1
2
3
4
```

```
typedef enum {
	MSPTI_ACTIVITY_MEMORY_UNKNOWN = 0,    // 内部预留，未定义
	MSPTI_ACTIVITY_MEMORY_DEVICE = 1,    // 设备内存
} msptiActivityMemoryKind;

```
|  |  |
| --- | --- |
**父主题：**[Enumeration类型](atlasprofiling_16_0258.html)