---
title: "概述"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/msquickstart/atlasquick_infer_0001.html"
date_collected: "2026-05-04"
category: "quickstart"
original_path: "zh/mindstudio/830/msquickstart/atlasquick_infer_0001.html"
---

# 概述

MindStudio推理工具链为开发者提供一站式推理开发工具，致力于加速模型问题定位效率，提升模型推理性能。

本文档以Llama-3.1-8B-Instruct模型为例，介绍针对大模型推理工具链中的模型量化、推理数据dump、自动精度比对、性能调优等工具的应用。

#### 使用说明

在大模型推理过程中，各工具的功能说明如表1所示。
**表1**推理工具功能说明
工具

功能说明

模型量化（msModelSlim）

提供模型压缩技术，通过降低模型权重和激活值的数值精度，有效减少模型的存储内存占用和计算需求。通常会将高位浮点数转换为低位定点数，从而直接减少模型权重的体积。模型量化工具的输入为能够正常运行的模型和数据，输出为一个可以使用的量化权重和量化因子。

数据落盘（msit llm dump）

提供加速库模型推理过程中产生的中间数据的dump能力，落盘的数据用于进行后续的精度比对。

精度比对（msit llm compare）

提供一键式精度比对功能，支持快速实现推理场景的整网精度比对。

性能调优

采集和分析运行在昇腾AI处理器上的AI任务各个运行阶段的关键性能指标。

服务化调优

提供全链路性能剖析，清晰展示框架调度、模型推理等环节的表现，帮助用户快速找到性能瓶颈（帮助判断是框架问题还是模型问题），从而有效提升服务性能。

MindStudio Insight

将通过性能调优工具采集到的性能数据，使用MindStudio Insight进行可视化呈现，快速定位软、硬件性能瓶颈，提升AI任务性能分析的效率。
|  |  |
| --- | --- |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |

#### 环境准备

- 部署开发环境，可参见《MindIE安装指南》的“安装MindIE > 方式一：镜像部署方式”章节内容部署。
- [安装msit工具包，安装过程请参见msit工具安装](https://gitcode.com/Ascend/msit/tree/master/msit/docs/install)文档进行安装，推荐使用源代码安装方式。
- [安装msModelSlim软件，请参见msModelSlim](https://gitcode.com/Ascend/msmodelslim/blob/master/docs/zh/install_guide.md)下载msModelSlim软件包进行安装。
- [安装大模型推理精度工具，请参见大模型推理精度工具（Large Language Model Debug Tool）](https://gitcode.com/Ascend/msit/tree/master/msit/docs/llm)进行安装。
- [安装配套版本的CANN Toolkit开发套件包和ops算子包并配置CANN环境变量，请参见《CANN 软件安装指南](https://www.hiascend.com/document/detail/zh/canncommercial/850/softwareinst/instg/instg_0000.html?Mode=PmIns&InstallType=local&OS=openEuler)》。
- [安装MindStudio Insight工具，请参见《MindStudio Insight工具用户指南](https://www.hiascend.com/document/detail/zh/mindstudio/830/GUI_baseddevelopmenttool/msascendinsightug/Insight_userguide_0002.html)[》中的“安装与卸载](https://www.hiascend.com/document/detail/zh/mindstudio/830/GUI_baseddevelopmenttool/msascendinsightug/Insight_userguide_0005.html)”章节，选择合适的环境进行安装。
**父主题：**[大模型推理工具快速入门](tools_qucikstart_0004.html)