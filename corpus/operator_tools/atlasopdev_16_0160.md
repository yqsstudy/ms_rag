---
title: "内存通路吞吐率波形图"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0160.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0160.html"
---

# 内存通路吞吐率波形图

[通过msprof op simulator](atlasopdev_16_00851.html#ZH-CN_TOPIC_0000002536920559__zh-cn_topic_0000002534426389_section8684154219309)生成的visualize_data.bin文件可通过MindStudio Insight进行可视化呈现。界面支持查看算子MTE日志通路的内存带宽在时序上的统计分析能力，可协助开发者识别算子各阶段的带宽使用状况，并分析带宽优化的可行性。具体特性支持情况请参见图1。

- [若要使用MindStudio Insight进行查看时，需要单独安装MindStudio Insight软件包，具体下载链接请参见“安装与卸载](https://www.hiascend.com/document/detail/zh/mindstudio/830/GUI_baseddevelopmenttool/msascendinsightug/Insight_userguide_0005.html)”。
- 将visualize_data.bin文件导入MindStudio Insight的具体操作请参考导入性能数据。
- [MindStudio Insight具体操作和详细字段解释请参考源码（Source）](https://www.hiascend.com/document/detail/zh/mindstudio/830/GUI_baseddevelopmenttool/msascendinsightug/Insight_userguide_0068.html)。
- 内存通路吞吐率波形图功能仅适用于
 Atlas A2 训练系列产品
 /
 Atlas A2 推理系列产品
 和
 Atlas A3 训练系列产品
 /
 Atlas A3 推理系列产品
 。
- 此功能默认不开启，--core-id设置对该功能不生效。

#### 内存通路吞吐率波形图
**图1**内存通路吞吐率波形图
![](figure/zh-cn_image_0000002534506565.png "点击放大")

- 展示各种类型内存通路（当前仅展示GM_TO_L1、GM_TO_TOTAL、GM_TO_UB、L1_TO_GM、TOTAL_TO_GM、UB_TO_GM六个通路）的数据吞吐率（单位为MB/s）。例如，GM_TO_UB表示从GM搬运到UB的吞吐率，GM_TO_TOTAL表示从GM搬运到各内存单元的吞吐率。
- 结合MTE相关指令，观察执行相关命令时的吞吐率，协助用户识别算子性能问题。
  - 吞吐率计算所采用的数据是某一个指令多次请求结束时的数据。
  - 吞吐率波形图可能出现在某指令的起始时间和结束时间范围内（包含起始时间和结束时间）。例如，持续时间为1~3微秒的指令，吞吐率数据可能分散在1~2微秒、2~3微秒及3~4微秒三个柱状图内。

**父主题：**[算子调优（msProf）](atlasopdev_16_0081.html)