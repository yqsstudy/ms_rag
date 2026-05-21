---
title: "通算流水图"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0139.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0139.html"
---

# 通算流水图

[通过msprof op](atlasopdev_16_00851.html#ZH-CN_TOPIC_0000002536920559__zh-cn_topic_0000002534426389_section0449171943115)对通算融合算子进行调优后，生成的trace.json和visualize_data.bin文件可通过MindStudio Insight进行可视化呈现，能够直观看到通算运行情况、指令耗时等信息，协助开发者识别通算瓶颈。当前仅支持MC2和LCCL类型的通算融合算子。

- [若要使用MindStudio Insight进行查看时，需要单独安装MindStudio Insight软件包，具体下载链接请参见“安装与卸载](https://www.hiascend.com/document/detail/zh/mindstudio/830/GUI_baseddevelopmenttool/msascendinsightug/Insight_userguide_0005.html)”。
- 将visualize_data.bin文件导入MindStudio Insight的具体操作请参考导入性能数据。
- [MindStudio Insight具体操作和详细字段解释请参考《MindStudio Insight工具用户指南](https://www.hiascend.com/document/detail/zh/mindstudio/830/GUI_baseddevelopmenttool/msascendinsightug/Insight_userguide_0002.html)[》的“系统调优 > 时间线（Timeline）](https://www.hiascend.com/document/detail/zh/mindstudio/830/GUI_baseddevelopmenttool/msascendinsightug/Insight_userguide_0034.html)”章节。
- 添加-g编译选项会在生成的二进制文件中附带调试信息，建议限制带有调试信息的用户程序的访问权限，确保只有授权人员可以访问该二进制文件。

- Chrome浏览器
[在Chrome浏览器中输入“chrome://tracing”地址，并将通过msprof op](atlasopdev_16_00851.html#ZH-CN_TOPIC_0000002536920559__zh-cn_topic_0000002534426389_section0449171943115)生成的通算流水图文件（trace.json）拖到空白处打开，键盘上输入快捷键（W：放大，S：缩小，A：左移，D：右移）可进行查看。关键字段说明如表1。
**表1**关键字段说明
字段名

字段功能

MC2算子

LCCL算子

AI CORE

算子在AI CORE上的整体运行情况。

支持

支持

AI CPU

算子在AI CPU上的整体运行情况。

支持

不支持

TURN

算子在AI CPU上不同通信轮次的流水。

支持

不支持

AIC BLOCK

算子在AI CORE各Cube核上的整体运行情况和关键接口调用情况。

支持

支持

AIV BLOCK

算子在AI CORE各Vector核上的整体运行情况和关键接口调用情况。

支持

支持

HCCL

通过HCCL通信的算子在多卡间的集合通信流水。

支持

不支持

HCCL TASK

通过HCCL通信的算子在多卡间的集合通信任务执行流水。

支持

不支持
|  |  |  |  |
| --- | --- | --- | --- |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |

- [MindStudio Insight
 
 通过msprof op](atlasopdev_16_00851.html#ZH-CN_TOPIC_0000002536920559__zh-cn_topic_0000002534426389_section0449171943115)**生成的trace.json文件或visualize_data.bin文件可导入MindStudio Insight进行可视化呈现。
 
 图1**通算流水图
![](figure/zh-cn_image_0000002502746480.png "点击放大")

  - 展示算子在AI CPU和AI CORE的耗时掩盖情况，用于评估通算融合算子的性能。
  - 展示算子在AI CPU上的不同通信轮次的流水。
  - 展示算子在各BLOCK上的运行时间及关键接口调用流水。
  - 展示通过HCCL通信的算子在多卡间运行时的集合通信流水及集合通信任务流水。
    - MC2算子支持对
 Atlas A2 训练系列产品
 /
 Atlas A2 推理系列产品
 的AllReduce、AllGather、ReduceScatter、AlltoAll等接口及
 Atlas A3 训练系列产品
 /
 Atlas A3 推理系列产品
 的AllGather、ReduceScatter、AlltoAllV等接口进行调用，具体介绍请参见中的“高阶API >HCCL通信类> HCCL Kernel侧接口”章节，添加-g编译选项后，单击具体接口将会展示代码行的调用栈。
    - MC2算子和LCCL算子的支持情况请参考表1。

**父主题：**[算子调优（msProf）](atlasopdev_16_0081.html)