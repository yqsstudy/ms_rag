---
title: "msptiActivityKind"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0238.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0238.html"
---

# msptiActivityKind

[msptiActivityKind为HcclData](atlasprofiling_16_0232.html#ZH-CN_TOPIC_0000002536158443)[、KernelData](atlasprofiling_16_0233.html#ZH-CN_TOPIC_0000002504198628)[、MarkerData](atlasprofiling_16_0234.html#ZH-CN_TOPIC_0000002504358464)[和RangeMarkerData](atlasprofiling_16_0235.html#ZH-CN_TOPIC_0000002536038417)调用的枚举类。

MSPTI通过msptiActivityKind对所有能采集到的数据进行分类，每个枚举值对应一个数据的结构体类型。定义如下：

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
class MsptiActivityKind(Enum):
	MSPTI_ACTIVITY_KIND_INVALID = 0   # 非法值
	MSPTI_ACTIVITY_KIND_MARKER = 1   # MSPTI打点能力（标记瞬时时刻）的Activity Record类型，支持最大打点个数为uint32_t最大值，返回结构体或
	MSPTI_ACTIVITY_KIND_KERNEL = 2   # aclnn场景下，计算类算子信息采集的Activity Record类型，返回结构体
	MSPTI_ACTIVITY_KIND_API = 3   # 预留参数，暂未开放
	MSPTI_ACTIVITY_KIND_HCCL = 4   # 通信算子采集Activity Record类型，返回结构体
	MSPTI_ACTIVITY_KIND_COUNT
	MSPTI_ACTIVITY_KIND_FORCE_INT = 0x7fffffff

```
|  |  |
| --- | --- |
**父主题：**[Enumeration类型](atlasprofiling_16_0236.html)