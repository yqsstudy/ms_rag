---
title: "快慢卡定点精确分析法"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_032.html"
date_collected: "2026-05-04"
category: "llm_cases"
original_path: "zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_032.html"
---

# 快慢卡定点精确分析法

可以从MindStudio Insight时间线（Timeline）页签，快速定位快慢卡产生差异的根源。
**图1**
定点精确分析方法
#### 定位点

首先要找到产生快慢卡的问题点，进入通信页签的通信算子缩略图，迭代ID选择靠后的ID，并且首先观察差异最大的集合通信算子，从快慢卡影响最大的地方入手，右键跳转到对应的通信位置。以绿色算子为例，如图2所示。
**图2**
定位点
#### 定区间

1. 放大通信算子。找到需要对比的卡（找到耗时差距最大的卡，如0和3卡），如图3所示。**图3**
定区间1
2. **在通信算子上单击鼠标右键，选择“跳转至时间线视图”，跳转到时间线（Timeline）的对应位置。建议在两张卡HCCL通信算子所对应Python侧下发API的开头做一个旗子标记。图4**
定区间2
3. 找到开始产生快慢卡问题的地方（白线位置），作为对比区域的开始，以两张卡的旗子标记分别作为两张卡对比区间的结束，分别得到快卡区域和慢卡区域，如图5所示。**图5**
查找产生快慢卡的地方

#### 找不同

分别在快卡区域和慢卡区域对比不同部分，从而进一步找到产生差异的具体原因。

以图6为例，造成快慢卡的地方主要有三块，分别是1和4、2和5以及3和6区域。
**图6**
示例图
至此已经定位到快慢卡的问题点，下一步就需要根据算子和代码定位快慢卡的根因。
**父主题：**[快慢卡问题定位方法](toolsample6_030.html)