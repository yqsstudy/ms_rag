---
title: "Roofline瓶颈分析图"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0119.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0119.html"
---

# Roofline瓶颈分析图

[通过msprof op](atlasopdev_16_00851.html#ZH-CN_TOPIC_0000002536920559__zh-cn_topic_0000002534426389_section0449171943115)生成的visualize_data.bin文件可通过MindStudio Insight进行可视化呈现，Roofline瓶颈分析图可构建出处理器的性能模型，然后利用该性能模型快速评估出算子的理论性能极限，协助开发者快速识别瓶颈类型。

- [若要使用MindStudio Insight进行查看时，需要单独安装MindStudio Insight软件包，具体下载链接请参见“安装与卸载](https://www.hiascend.com/document/detail/zh/mindstudio/830/GUI_baseddevelopmenttool/msascendinsightug/Insight_userguide_0005.html)”。
- 将visualize_data.bin文件导入MindStudio Insight的具体操作请参考导入性能数据。
- [MindStudio Insight具体操作请参考详情（Details）](https://www.hiascend.com/document/detail/zh/mindstudio/830/GUI_baseddevelopmenttool/msascendinsightug/Insight_userguide_0071.html)。

#### 硬件支持情况

[通过msprof op](atlasopdev_16_00851.html#ZH-CN_TOPIC_0000002536920559__zh-cn_topic_0000002534426389_section0449171943115)生成的visualize_data.bin文件可导入MindStudio Insight进行可视化呈现，并针对不同的硬件以及算子类型会生成不同的Roofline分析视图。

- **Atlas 推理系列产品
 的Roofline瓶颈分析图中仅有内存单元视图。
 
 图1**
![](figure/zh-cn_image_0000002534506581.png "点击放大")Atlas 推理系列产品
 Roofline瓶颈分析图
- Atlas A3 训练系列产品
 /
 Atlas A3 推理系列产品
 和
 Atlas A2 训练系列产品
 /
 Atlas A2 推理系列产品
 根据算子类型不同而产生不同的视图，具体请参见表1**。
 
 图2**Atlas A3 训练系列产品
 /
 Atlas A3 推理系列产品
 和
 Atlas A2 训练系列产品
 /
 Atlas A2 推理系列产品
 Roofline瓶颈分析图
![](figure/zh-cn_image_0000002534426545.png "点击放大")
**表1**Atlas A3 训练系列产品
 /
 Atlas A3 推理系列产品
 和
 Atlas A2 训练系列产品
 /
 Atlas A2 推理系列产品
 支持Roofline视图情况列表
Roofline视图类型

Vector算子

Cube算子

Mix算子

GM/L2视图

√

√

√

Vector内存单元视图

√

-

√

Vector内存通路视图

√

-

√

Vector Pipeline视图

√

-

√

Cube内存单元视图

-

√

√

Cube内存通路视图

-

√

√

Cube Pipeline视图

-

√

√
|  |  |  |  |
| --- | --- | --- | --- |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |

#### 功能介绍

每个单元/通路的Roofline性能分析结果由横轴、纵轴、屋顶线、带宽斜线和实际运行坐标点组成，具体请参见图3。
**图3**
![](figure/zh-cn_image_0000002534426541.png "点击放大")Roofline示意图
- 横轴：代表算术强度（Arithmetic Intensity），即某一单元或通路中总的浮点运算次数与总的访存数据量之比，单位为Ops/Byte。
- 纵轴：表示计算性能（Performance），即每秒可执行的浮点操作数，单位为 TOps/s。
- 屋顶线：指图中顶部的水平线，代表NPU的理论最大计算性能。无论算术强度如何提高，应用的实际性能都不可能超过硬件上限。
- 带宽斜线：指图中与屋顶线相交的斜线，其与纵轴的交点取决于理论最大带宽。当理论最大带宽乘以算术强度小于NPU理论最大计算性能时，能达到的最大算力随算术强度的增加而线性增长。
屋顶线和带宽斜线组合成算子能达到的理论最大算力，可以概括为min（NPU理论最大计算性能，理论最大带宽*实际算术强度）。

- 实际运行坐标点的参数构成请参见表2。**表2**实际运行坐标点简介
坐标参数

简介

带宽（Bandwidth）

该单元/通路的理论最大带宽。

算术强度（Arithmetic Intensity）

算子实际运行时的算术强度，即横轴坐标值。

性能（Performance）

算子实际运行时的计算性能，即纵轴坐标值。

性能百分比（Performance Ratio）

算子实际运行时的计算性能与当前数据量下的理论最大计算性能比值，即图中a/b的百分比。
|  |  |
| --- | --- |
|  |  |
|  |  |
|  |  |
|  |  |

Roofline分析视图分析算子的性能百分比，并提供以下客观分析结果：
- 算子性能百分比大于80%时，按照所在区域进行提示，有以下两种情况。
  - Compute Bound：计算瓶颈。
  - Memory Bound：内存瓶颈。

- 算子性能百分比小于80%，Bound类型为Latency Bound，有以下三种情况：
  - 若最大的pipeline ratio小于80%，提示latency bound:pipeline caused。
  - 若最大的pipeline ratio大于80%，需识别最大pipeline ratio的类型。
    - 若最大pipeline ratio的类型是compute pipeline (cube ratio、vector ratio、scalar ratio)，提示latency bound:compute caused。
    - 若最大pipeline ratio的类型是memory pipeline(MTE1 ratio、MTE2 ratio、MTE3 ratio)，提示latency bound:memory caused。

**父主题：**[算子调优（msProf）](atlasopdev_16_0081.html)