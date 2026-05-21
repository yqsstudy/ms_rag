---
title: "总体说明"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0101.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0101.html"
---

# 总体说明

#### 接口简介

msServiceProfiler模块提供推理服务化性能数据采集（Python）接口，用于实现采集服务化调优场景性能数据。

[推理服务化性能数据采集接口功能介绍和使用示例请参见数据采集](atlasprofiling_16_0029.html#ZH-CN_TOPIC_0000002504198516)。

Python接口导入：from ms_service_profiler import Profiler, Level

#### 接口列表

具体接口如下：
**表1**服务化性能数据采集API（Python）
接口

说明

init

初始化。

__enter__/__exit__

在进入的时候，自动调用span_start函数，用于记录过程开始的时间点；在退出的时候，自动调用span_end函数，用于记录过程的结束时间点。

span_start

记录一个过程的开始节点。

span_end

记录一个过程的结束节点。

event

记录一个事件。

link

记录不同资源之间的关联。

metric

记录一个指标类数值。

metric_inc

记录一个指标类的增量数值。

metric_scope

定义一个指标类的作用范围。

metric_scope_as_req_id

定义一个指标类的作用范围为请求级别。

launch

正式将该请求记录落盘。

attr

添加属性，返回当前对象，支持链式调用。

domain

指定该数据的域，相同域的记录在trace数据中归为一类。

res

添加资源ID，数据和timeline根据资源ID进行关联。

get_msg

获取当前记录的数据。
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
**父主题：**[服务化调优](atlasprofiling_16_0100.html)