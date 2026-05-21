---
title: "msptiActivityMemoryOperationType"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0262.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0262.html"
---

# msptiActivityMemoryOperationType

内存操作类型。

[msptiActivityMemoryOperationType为msptiActivityMemory](atlasprofiling_16_0273.html#ZH-CN_TOPIC_0000002504198648)调用的枚举类，定义如下：

```
1
2
3
4
```

```
typedef enum {
	MSPTI_ACTIVITY_MEMORY_OPERATION_TYPE_ALLOCATION = 0,    // 分配内存
	MSPTI_ACTIVITY_MEMORY_OPERATION_TYPE_RELEASE = 1    // 释放内存
} msptiActivityMemoryOperationType;

```
|  |  |
| --- | --- |
**父主题：**[Enumeration类型](atlasprofiling_16_0258.html)