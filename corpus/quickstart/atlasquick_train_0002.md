---
title: "概述"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/msquickstart/atlasquick_train_0002.html"
date_collected: "2026-05-04"
category: "quickstart"
original_path: "zh/mindstudio/830/msquickstart/atlasquick_train_0002.html"
---

# 概述

本文介绍训练场景开发工具快速入门，主要针对训练开发流程中的模型开发&迁移、模型精度调试和模型性能调优环节分别使用的开发工具进行介绍。

主要工具介绍：

- msprobe工具：
基于昇腾开发的大模型或者是从GPU迁移到昇腾NPU环境的大模型，在训练过程中可能出现精度溢出、loss曲线跑飞或不收敛等异常问题。由于训练loss等指标无法精确定位问题模块，本文提供了msprobe（MindStudio Probe，精度调试工具）进行快速定界。精度调试工具在下文均简称为msprobe。

msprobe为mstt工具链的精度工具，通过分别对标杆环境（如已调试好的CPU、GPU或昇腾NPU等环境）和昇腾NPU环境下的训练精度数据进行采集和比对，从而找出差异点。

[msprobe工具包含众多功能，介绍请参见《msprobe使用手册](https://gitcode.com/Ascend/mstt/tree/br_release_MindStudio_8.3.0_20261231/debug/accuracy_tools/msprobe)》。

- MindSpore Profiler接口工具：MindSpore训练场景下的性能数据采集。
- Ascend PyTorch Profiler接口工具：PyTorch训练场景下的性能数据采集。
- msprof-analyze工具：统计、分析以及输出相关的调优建议。
- MindStudio Insight工具：对性能数据进行可视化展示。

#### 使用流程
**表1**主要流程和工具操作流程
流程

使用工具和操作流程

模型开发&迁移

MindSpore训练场景暂未提供迁移工具，本文以直接在昇腾NPU环境开发的训练脚本为例。

PyTorch训练场景使用分析迁移工具进行GPU向昇腾NPU环境迁移。

模型精度调试

使用msprobe工具在模型精度调试中主要执行如下操作：

1. 训练前配置检查
识别两个环境影响精度的配置差异。

2. （可选）训练状态监控
监控训练过程中计算，通信，优化器等部分出现的异常情况。

3. 精度数据采集
采集训练过程中的API或Module层级前反向输入输出数据。

4. 精度预检
扫描API数据，找出存在精度问题的API。

5. 精度比对
对比NPU侧和标杆环境的API数据，快速定位精度问题。

模型性能调优

MindSpore训练场景在模型性能调优中主要执行如下操作：

1. 性能数据采集：MindSpore Profiler接口工具。
2. 性能数据分析：msprof-analyze工具。
3. 性能数据可视化展示：MindStudio Insight工具。

PyTorch训练场景在模型性能调优中主要执行如下操作：

1. 性能数据采集：Ascend PyTorch Profiler接口工具。
2. 性能数据分析：msprof-analyze工具。
3. 性能数据可视化展示：MindStudio Insight工具。
|  |  |
| --- | --- |
|  |  |
|  |  |
|  |  |

#### 环境准备

1. [准备一台基于Atlas 训练系列产品的训练服务器，并安装NPU驱动和固件](https://www.hiascend.com/document/detail/zh/canncommercial/850/softwareinst/instg/instg_0005.html?Mode=PmIns&InstallType=local&OS=openEuler)。
2. [安装配套版本的CANN Toolkit开发套件包和ops算子包并配置CANN环境变量，请参见《CANN 软件安装指南](https://www.hiascend.com/document/detail/zh/canncommercial/850/softwareinst/instg/instg_0000.html?Mode=PmIns&InstallType=local&OS=openEuler)》。
3. 安装框架。
[MindSpore训练场景以安装2.6.0和2.7.0版本为例，具体操作请参见《MindSpore安装指南](https://www.mindspore.cn/install/)》。

[PyTorch训练场景以安装2.1.0版本为例，具体操作请参见《Ascend Extension for PyTorch 软件安装指南](https://www.hiascend.com/document/detail/zh/Pytorch/730/configandinstg/instg/docs/zh/installation_guide/installation_description.md)[》的“安装PyTorch](https://www.hiascend.com/document/detail/zh/Pytorch/730/configandinstg/instg/docs/zh/installation_guide/installation_via_binary_package.md)”章节。

4. 配置环境变量。
***安装CANN软件后，使用CANN运行用户进行编译、运行时，需要以CANN运行用户登录环境，执行source ${install_path}*/set_env.sh**命令设置环境变量。其中${install_path}为CANN软件的安装目录，例如：/usr/local/Ascend/cann。

**父主题：**[训练场景工具快速入门](tools_qucikstart_0002.html)