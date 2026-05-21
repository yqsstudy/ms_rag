---
title: "计算内存热力图"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0086.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0086.html"
---

# 计算内存热力图

[通过msprof op](atlasopdev_16_00851.html#ZH-CN_TOPIC_0000002536920559__zh-cn_topic_0000002534426389_section0449171943115)生成的visualize_data.bin文件可通过MindStudio Insight进行可视化呈现，界面将会以资源维度展示算子基础信息、计算负载分析和内存负载分析的数据，协助开发者以全局视角识别资源瓶颈。

- [若要使用MindStudio Insight进行查看时，需要单独安装MindStudio Insight软件包，具体下载链接请参见“安装与卸载](https://www.hiascend.com/document/detail/zh/mindstudio/830/GUI_baseddevelopmenttool/msascendinsightug/Insight_userguide_0005.html)”。
- 将visualize_data.bin文件导入MindStudio Insight的具体操作请参考导入性能数据。
- [MindStudio Insight具体操作请参考详情（Details）](https://www.hiascend.com/document/detail/zh/mindstudio/830/GUI_baseddevelopmenttool/msascendinsightug/Insight_userguide_0071.html)。
**图1**
![](figure/zh-cn_image_0000002534506521.png "点击放大")详情界面1
- 提供核间负载分析图（Core Occupancy），以数据窗格的方式呈现各物理单核的耗时、总数据吞吐量及Cache命中率，帮助开发人员提升物理核的使用效率。
  - 仅
 Atlas A3 训练系列产品
 /
 Atlas A3 推理系列产品
 和
 Atlas A2 训练系列产品
 /
 Atlas A2 推理系列产品
 支持该功能。
  - 具体展示的核数与实际使用的硬件有关。

- [Roofline瓶颈分析图（Roofline）：具体介绍请参见Roofline瓶颈分析图](atlasopdev_16_0119.html#ZH-CN_TOPIC_0000002505040630)。
- 提供计算负载分析（Compute Workload Analysis），以柱状图和数据表格的方式呈现计算负载数据，帮助开发人员分析Cube/Vector计算资源是否得到了充分利用。
- 提供内存负载分析（Memory Workload Analysis），支持展示MTE各通路的活跃带宽值（未开启动态插桩不显示Cube上的MTE1和MTE2通路的活跃带宽）。通过内存热力图和数据窗格，直观呈现各通路的请求数、搬运带宽与利用率。帮助开发人员分析可能存在瓶颈的通路。
  - 数据窗格呈现的内容会随算子类型而变化。
  - 活跃带宽值的功能不适用于
 Atlas 推理系列产品
 。
  - Atlas A3 训练系列产品
 /
 Atlas A3 推理系列产品
 暂不支持峰值（最大带宽占比）展示。

**父主题：**[算子调优（msProf）](atlasopdev_16_0081.html)