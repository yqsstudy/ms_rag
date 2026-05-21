---
title: "msptiCommunicationDataType"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0266.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0266.html"
---

# msptiCommunicationDataType

记录通信算子的数据类型。

[msptiCommunicationDataType为msptiActivityCommunication](atlasprofiling_16_0277.html#ZH-CN_TOPIC_0000002504198650)调用的枚举类，定义如下：

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
12
13
14
15
16
```

```
typedef enum {
    MSPTI_ACTIVITY_COMMUNICATION_INT8 = 0,   // INT8类型
    MSPTI_ACTIVITY_COMMUNICATION_INT16 = 1,   // INT16类型
    MSPTI_ACTIVITY_COMMUNICATION_INT32 = 2,   // INT32类型
    MSPTI_ACTIVITY_COMMUNICATION_FP16 = 3,   // FP16类型
    MSPTI_ACTIVITY_COMMUNICATION_FP32 = 4,   // FP32类型
    MSPTI_ACTIVITY_COMMUNICATION_INT64 = 5,   // INT64类型
    MSPTI_ACTIVITY_COMMUNICATION_UINT64 = 6,   // UINT64类型
    MSPTI_ACTIVITY_COMMUNICATION_UINT8 = 7,   // UINT8类型
    MSPTI_ACTIVITY_COMMUNICATION_UINT16 = 8,   // UINT16类型
    MSPTI_ACTIVITY_COMMUNICATION_UINT32 = 9,   // UINT32类型
    MSPTI_ACTIVITY_COMMUNICATION_FP64 = 10,   // FP64类型
    MSPTI_ACTIVITY_COMMUNICATION_BFP16 = 11,   // BFP16类型
    MSPTI_ACTIVITY_COMMUNICATION_INT128 = 12,   // INT128类型
    MSPTI_ACTIVITY_COMMUNICATION_INVALID_TYPE = 0x0000FFFF
} msptiCommunicationDataType;

```
|  |  |
| --- | --- |
**父主题：**[Enumeration类型](atlasprofiling_16_0258.html)