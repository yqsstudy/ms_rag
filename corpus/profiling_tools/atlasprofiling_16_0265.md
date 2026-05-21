---
title: "msptiExternalCorrelationKind"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0265.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0265.html"
---

# msptiExternalCorrelationKind

支持关联的外部API的类型。

[msptiExternalCorrelationKind为msptiActivityPushExternalCorrelationId](atlasprofiling_16_0251.html#ZH-CN_TOPIC_0000002536038425)[和msptiActivityExternalCorrelation](atlasprofiling_16_0276.html#ZH-CN_TOPIC_0000002536158465)调用的枚举类，定义如下：

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
```

```
typedef enum {
	MSPTI_EXTERNAL_CORRELATION_KIND_INVALID = 0,   // 非法值
	MSPTI_EXTERNAL_CORRELATION_KIND_UNKNOWN = 1,   // MSPTI未知的外部API
	MSPTI_EXTERNAL_CORRELATION_KIND_CUSTOM0 = 2,   // 外部API为CUSTOM0
	MSPTI_EXTERNAL_CORRELATION_KIND_CUSTOM1 = 3,   // 外部API为CUSTOM1
	MSPTI_EXTERNAL_CORRELATION_KIND_CUSTOM2 = 4,   // 外部API为CUSTOM2
	MSPTI_EXTERNAL_CORRELATION_KIND_SIZE,   // 在此行之前添加新的类型
	MSPTI_EXTERNAL_CORRELATION_KIND_FORCE_INT = 0x7fffffff,
} msptiExternalCorrelationKind;

```
|  |  |
| --- | --- |
**父主题：**[Enumeration类型](atlasprofiling_16_0258.html)