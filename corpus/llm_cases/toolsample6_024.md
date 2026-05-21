---
title: "算子（Operator）"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_024.html"
date_collected: "2026-05-04"
category: "llm_cases"
original_path: "zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_024.html"
---

# 算子（Operator）

算子（Operator）界面展示计算算子和通信算子耗时统计，常用功能如下：

- 按类型统计，用于观察Top耗时算子占比，尤其是转换类等低效算子是否占比过高。
- 按加速器核分组统计，观察AI CPU类算子与vector类算子是否耗时占比过高。
- 按输入Shape统计计算算子，观察算子是否会在特定Shape下劣化。
- 可切换展示耗时Top15或全部算子，如图1所示。

[具体定位与优化方法，可参考算子性能问题优化方案](toolsample6_048.html)。
**图1**
算子界面
[算子（Operator）界面还支持两卡间的比对功能，详情请参见《MindStudio Insight工具用户指南](https://www.hiascend.com/document/detail/zh/mindstudio/830/GUI_baseddevelopmenttool/msascendinsightug/Insight_userguide_0002.html)》的使用说明章节。

#### 典型案例：利用算子比对功能快速定位计算性能劣化原因

问题背景：相同模型在不同机器上部署，计算性能劣化（每step约80ms），需定位原因。

1. 将两卡的性能数据移动至同一父目录，使用MindStudio Insight打开该父目录。
2. [参见《MindStudio Insight工具用户指南](https://www.hiascend.com/document/detail/zh/mindstudio/830/GUI_baseddevelopmenttool/msascendinsightug/Insight_userguide_0002.html)》的使用说明章节设置两卡间数据比对。
3. 已知慢卡相比快卡单Step计算耗时多出约80ms。开启比对模式后，在“算子详情”中，按照“总耗时”进行排序，如图2所示。观察可发现，计算时间差异主要来源是Matmul算子，在数量一致的前提下（数量差为0），总耗时相差约74ms，为主要耗时差异来源。
**图2**
算子卡间比对

4. 进一步按相同Shape对比，可以看到，相同类型（MatmulV3）不同Shape算子有不同程度劣化，各个Shape下，慢卡Matmul稳定劣化于快卡，如图3所示。
**图3**
按Shape比对

5. 经排查，最终确认是不同机器片上内存颗粒差异，Matmul是访存密集型算子，在不同机器上计算通信带宽抢占程度不同导致。
**父主题：**[单卡性能分析](toolsample6_021.html)