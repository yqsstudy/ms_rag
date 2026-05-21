---
title: "集群训练场景性能分析"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0303.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0303.html"
---

# 集群训练场景性能分析

#### 场景介绍

一个集群是由多个节点组成，每个节点都有单独的系统，通过管理界面统一管理。在集群场景执行采集每个节点的性能数据，每个节点均生成一个PROF_XXX目录并进行预解析，将各个节点的PROF_XXX目录汇总到OBS。用户需要手动将OBS汇总的所有PROF_XXX目录拷贝到可以展示和分析集群数据的环境下进行展示和分析。

当前支持集群数据展示和分析的工具为：MindStudio Insight。

#### 性能数据采集流程

性能数据采集总体流程如下图所示。
**图1**
性能数据采集流程
#### 环境搭建

- 集群场景请用户自行搭建。
- [根据需要在对应的节点上安装合适的CANN软件包，请参见《CANN 软件安装指南](https://www.hiascend.com/document/detail/zh/canncommercial/850/softwareinst/instg/instg_0000.html?Mode=PmIns&InstallType=local&OS=openEuler)》。
- [安装MindStudio Insight工具，详见《MindStudio Insight工具用户指南](https://www.hiascend.com/document/detail/zh/mindstudio/830/GUI_baseddevelopmenttool/msascendinsightug/Insight_userguide_0002.html)》。

#### 约束

集群场景执行性能数据采集最大支持采集128个节点（如果每个节点配置8个Device，即最大支持1024个Device）的性能数据。

#### 性能数据采集

完成环境搭建后，集群场景可参考以下方式进行性能数据采集。

- [使用性能数据采集和自动解析](atlasprofiling_16_0007.html#ZH-CN_TOPIC_0000002536038281)进行性能数据采集。
- 使用Ascend PyTorch Profiler接口采集PyTorch性能数据。
  1. [参见《PyTorch 训练模型迁移调优指南](https://www.hiascend.com/document/detail/zh/Pytorch/730/ptmoddevg/trainingmigrguide/PT_LMTMOG_0002.html)[》中的“模型迁移](https://www.hiascend.com/document/detail/zh/Pytorch/730/ptmoddevg/trainingmigrguide/PT_LMTMOG_0013.html)”搭建分布式训练环境，准备迁移后的分布式训练脚本。
  2. [参见PyTorch训练场景性能分析快速入门](atlasprofiling_16_0004.html#ZH-CN_TOPIC_0000002536158311)修改训练脚本，并拉起分布式训练进行数据采集。

#### 数据展示

[集群场景的性能数据需要通过MindStudio Insight工具进行界面化展示，详见《MindStudio Insight工具用户指南](https://www.hiascend.com/document/detail/zh/mindstudio/830/GUI_baseddevelopmenttool/msascendinsightug/Insight_userguide_0002.html)》。
**父主题：**[附录](atlasprofiling_16_0209.html)