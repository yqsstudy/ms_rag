---
title: "总体说明"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0060.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0060.html"
---

# 总体说明

#### 接口简介

msServiceProfiler模块提供推理服务化性能数据采集（C++）接口，用于采集服务化调优场景性能数据。

[推理服务化性能数据采集接口功能介绍和使用示例请参见数据采集](atlasprofiling_16_0029.html#ZH-CN_TOPIC_0000002504198516)。

头文件：${INSTALL_DIR}/include/msServiceProfiler/msServiceProfiler.h

库文件：${INSTALL_DIR}/lib64/libms_service_profiler.so

${INSTALL_DIR}请替换为CANN软件安装后文件存储路径。若安装的Ascend-cann-toolkit软件包，以root安装举例，则安装后文件存储路径为：/usr/local/Ascend/ascend-toolkit/latest。

#### 接口列表

具体接口如下：
**表1**服务化性能数据采集API（C++）
接口

说明

IsEnable

判断是否使能采集数据。

SpanStart

记录一个过程的开始节点。

SpanEnd

记录一个过程的结束节点。

Metric

记录一个指标类数值。

MetricInc

记录一个指标类的增量数值。

MetricScope

定义一个指标类的作用范围。

MetricScopeAsReqID

定义一个指标类的作用范围为请求级别。

MetricScopeAsGlobal

定义一个指标类的作用范围为全局。

Launch

正式将该请求记录进行落盘。

Event

记录一个事件。

Link

记录不同资源之间的关联。

Attr系列

添加属性，返回当前对象，支持链式调用。

ArrayResource

添加数组类资源的关键属性。

Resource

添加资源ID，数据和timeline根据资源ID进行关联。

Domain

指定该数据的域，相同域的记录在trace数据中归为一类。

NumArrayAttr

添加数组属性，数组中仅支持数值。

ArrayAttr

通过回调函数自定义添加数组属性。

GetMsg

获取当前记录的数据。

宏定义

封装的采集语句。
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
**父主题：**[服务化调优](atlasprofiling_16_0059.html)