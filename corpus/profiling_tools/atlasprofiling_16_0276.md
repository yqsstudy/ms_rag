---
title: "msptiActivityExternalCorrelation"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0276.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0276.html"
---

# msptiActivityExternalCorrelation

[msptiActivityExternalCorrelation为Activity Record类型MSPTI_ACTIVITY_KIND_EXTERNAL_CORRELATION](atlasprofiling_16_0259.html#ZH-CN_TOPIC_0000002536038429)对应的结构体，用于关联Activity Record，定义如下：

```
1
2
3
4
5
6
```

```
typedef struct {
	msptiActivityKind kind;   // Activity Record类型MSPTI_ACTIVITY_KIND_EXTERNAL_CORRELATION
	msptiExternalCorrelationKind externalKind;   // 记录关联的外部API的类型
	uint64_t externalId;   // 关联外部API的关联ID
	uint64_t correlationId;   // 关联CANN API的关联ID
} msptiActivityExternalCorrelation;

```
|  |  |
| --- | --- |
**父主题：**[Data Structure类型](atlasprofiling_16_0267.html)