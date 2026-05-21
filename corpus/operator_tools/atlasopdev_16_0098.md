---
title: "OpBasicInfo（算子基础信息）"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0098.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0098.html"
---

# OpBasicInfo（算子基础信息）

算子基础信息数据OpBasicInfo.csv，包含算子名称，算子类型，Block Dim和耗时等信息。详情介绍请参见下表中的字段说明。
**图1**
![](figure/zh-cn_image_0000002502746514.png "点击放大")OpBasicInfo.csv文件
 
 
 
 关键字段说明如下。**表1**字段说明
字段名

字段解释

Op Name

算子名称。

Op Type

算子类型。

Task Duration(us)

Task耗时，包含调度到昇腾AI处理器的时间、昇腾AI处理器上的执行时间以及结束响应时间，单位us。

Block Dim

Task运行切分数量，对应Task运行时核数，开发者设置的算子执行逻辑核数。

Mix Block Dim

部分算子同时在Cube Core和Vector Core上执行，主昇腾AI处理器的blockDim在Block Dim字段描述，从昇腾AI处理器的blockDim在本字段描述。显示为N/A表示为非Mix融合算子。
说明：
此参数仅适用于
 Atlas A3 训练系列产品
 /
 Atlas A3 推理系列产品
 和
 Atlas A2 训练系列产品
 /
 Atlas A2 推理系列产品

Device ID

运行时使用昇腾AI处理器的ID。

PID

算子运行时的进程号。

Current Freq

昇腾AI处理器当前运行的频率。

Rated Freq

昇腾AI处理器的理论频率。
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
**父主题：**[msprof op](atlasopdev_16_0131.html)