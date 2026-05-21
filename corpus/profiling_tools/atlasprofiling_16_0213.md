---
title: "总体说明"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0213.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0213.html"
---

# 总体说明

#### 接口简介

Profiling模块提供MSPTI Python接口，用于实现采集各模块性能数据。

[MSPTI API的功能介绍和使用示例请参见MSPTI调优工具](atlasprofiling_16_0020.html#ZH-CN_TOPIC_0000002536158321)。

#### 接口列表

具体接口如下：
**表1**MSPTI Python API
接口

说明

**HcclMonitor**

HcclMonitor.start

标识通信算子性能数据采集的开始。

HcclMonitor.stop

标识通信算子性能数据采集的结束。

HcclMonitor.flush_all

调用回调函数，将缓冲区中的所有Activity数据写入用户内存。

HcclMonitor.set_buffer_size

在采集开始前设置Activity Buffer的大小。

**KernelMonitor**

KernelMonitor.start

标识Kernel性能数据采集的开始。

KernelMonitor.stop

标识Kernel性能数据采集的结束。

KernelMonitor.flush_all

调用回调函数，将缓冲区中的所有Activity数据写入用户内存。

KernelMonitor.set_buffer_size

在采集开始前设置Activity Buffer的大小。

**MstxMonitor**

MstxMonitor.start

标识数据采集mstx打点的开始。

MstxMonitor.stop

标识数据采集mstx打点的结束。

MstxMonitor.enable_domain

开启对应域打点的采集。

MstxMonitor.disable_domain

关闭对应域打点的采集。

MstxMonitor.flush_all

调用回调函数，将缓冲区中的所有Activity数据写入用户内存。

MstxMonitor.set_buffer_size

在采集开始前设置Activity Buffer的大小。

**Data Structure类型**

HcclData

Activity Record类型MSPTI_ACTIVITY_KIND_HCCL对应的结构体。

KernelData

Activity Record类型MSPTI_ACTIVITY_KIND_KERNEL对应的结构体。

MarkerData

Activity Record类型MSPTI_ACTIVITY_KIND_MARKER对应的结构体。

RangeMarkerData

Activity Record类型MSPTI_ACTIVITY_KIND_MARKER对应的结构体。

**Enumeration类型**

msptiResult

MSPTI返回的错误和结果代码。

msptiActivityKind

MSPTI支持的所有Activity类型。

msptiActivityFlag

Activity Record的活动标记。

msptiActivitySourceKind

标记Activity数据来源。
|  |  |
| --- | --- |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
**父主题：**[MSPTI Python API参考](atlasprofiling_16_0212.html)