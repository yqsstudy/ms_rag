---
title: "总体说明"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0242.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0242.html"
---

# 总体说明

#### 接口简介

Profiling模块提供MSPTI C接口，用于实现采集各模块性能数据。

[MSPTI API的功能介绍和使用示例请参见MSPTI调优工具](atlasprofiling_16_0020.html#ZH-CN_TOPIC_0000002536158321)。

头文件路径：${INSTALL_DIR}/include/mspti。

库文件路径：${INSTALL_DIR}/lib64/libmspti.so。

${INSTALL_DIR}请替换为CANN软件安装后文件存储路径。若安装的Ascend-cann-toolkit软件包，以root安装举例，则安装后文件存储路径为：/usr/local/Ascend/ascend-toolkit/latest。

#### 接口列表

具体接口如下：
**表1**Activity API
接口

说明

**Function类型**

msptiActivityRegisterCallbacks

向MSPTI注册回调函数，用于Activity Buffer处理。

msptiActivityEnable

用于使能指定Activity类型数据的采集。

msptiActivityDisable

停止收集特定类型的Activity Record。

msptiActivityGetNextRecord

依次从Activity Buffer获取Activity Record数据。

msptiActivityFlushAll

订阅者手动Flush Activity Buffer中记录的数据。

msptiActivityFlushPeriod

设置Flush的执行周期。

msptiActivityPushExternalCorrelationId

为调用线程推送外部关联ID。

msptiActivityPopExternalCorrelationId

为调用线程拉取外部关联ID。

**Typedef类型**

msptiBuffersCallbackRequestFunc

向MSPTI注册回调函数，申请Activity Buffer的存储空间。

msptiBuffersCallbackCompleteFunc

向MSPTI注册回调函数，释放Activity Buffer中的数据。

**E****numeration类型**

msptiActivityKind

MSPTI支持的所有Activity类型。

msptiActivityFlag

Activity Record的活动标记。

msptiActivitySourceKind

标记Activity数据来源。

msptiActivityMemoryOperationType

内存操作类型的枚举类。

msptiActivityMemoryKind

内存类型的枚举类。

msptiActivityMemcpyKind

内存拷贝类型的枚举类。

msptiExternalCorrelationKind

支持关联的外部API的类型。

msptiCommunicationDataType

记录通信算子的数据类型。

**Data Structure类型**

msptiActivity

Activity Record的基础结构体。

msptiActivityApi

Activity Record类型MSPTI_ACTIVITY_KIND_API对应的结构体。

msptiActivityHccl

Activity Record类型MSPTI_ACTIVITY_KIND_HCCL对应的结构体。

msptiActivityKernel

Activity Record类型MSPTI_ACTIVITY_KIND_KERNEL对应的结构体。

msptiActivityMarker

Activity Record类型MSPTI_ACTIVITY_KIND_MARKER对应的结构体。

msptiActivityMemory

Activity Record类型MSPTI_ACTIVITY_KIND_MEMORY对应的结构体。

msptiActivityMemset

Activity Record类型MSPTI_ACTIVITY_KIND_MEMSET对应的结构体。

msptiActivityMemcpy

Activity Record类型MSPTI_ACTIVITY_KIND_MEMCPY对应的结构体。

msptiActivityExternalCorrelation

Activity Record类型MSPTI_ACTIVITY_KIND_EXTERNAL_CORRELATION对应的结构体。

msptiActivityCommunication

Activity Record类型MSPTI_ACTIVITY_KIND_COMMUNICATION对应的结构体。

**Union类型**

msptiObjectId

用于识别Marker的进程ID、线程ID、Device ID、Stream ID。
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
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |

Activity Record：NPU的Profiling记录，使用结构体表示，如msptiActivityApi、msptiActivityMarker等。

Activity Buffer：用于缓存Activity Record数据，并将一个或多个Activity Record从MSPTI传输到客户端。用户根据业务需要提供空的Activity Buffer缓冲区，以确保Activity Record不会被遗漏。
**表2**Callback API
接口

说明

**Function类型**

msptiSubscribe

通过该接口向MSPTI注册回调函数。

msptiUnsubscribe

向MSPTI注销当前订阅者。

msptiEnableCallback

**为特定domain****和CallbackId**的订阅者开启或关闭回调。

msptiEnableDomain

**为特定domain**的订阅者开启或关闭所有回调。

**Typedef类型**

msptiCallbackFunc

回调函数类型。

msptiCallbackId

注册的Callback调用点ID。

msptiSubscriberHandle

订阅者的句柄。

**Enumeration类型**

msptiCallbackDomain

相关API函数或CANN驱动程序活动的回调点。

msptiApiCallbackSite

指定API调用中发出回调的点，如回调的开始和回调的结束。

msptiCallbackIdRuntime

Runtime API函数的索引定义。

msptiCallbackIdHccl

通信API函数的索引的简要定义。

**Data Structure类型**

msptiCallbackData

用于指定传递到回调函数的数据。
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
**表3**Result Codes
接口

说明

**Enumeration类型**

msptiResult

MSPTI返回的错误和结果代码。
|  |  |
| --- | --- |
|  |  |
|  |  |
**父主题：**[MSPTI C API参考](atlasprofiling_16_0241.html)