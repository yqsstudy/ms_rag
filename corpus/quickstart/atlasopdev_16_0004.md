---
title: "概述"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/msquickstart/atlasopdev_16_0004.html"
date_collected: "2026-05-04"
category: "quickstart"
original_path: "zh/mindstudio/830/msquickstart/atlasopdev_16_0004.html"
---

# 概述

MindStudio算子开发工具包含多个工具，如msKPP、msOpGen、msOpST、msSanitizer、msDebug和msProf等，本文档以一个简单样例介绍算子开发工具应用的全流程。

样例以单算子API调用方式为例，介绍如何使用算子开发工具进行算子设计、算子工程创建、算子功能测试、算子异常检测、算子调试及性能调优。

#### 环境准备

- [准备Atlas A2 训练系列产品/Atlas 800I A2 推理产品的服务器，并安装对应的驱动和固件，具体安装过程请参见安装NPU驱动和固件](https://www.hiascend.com/document/detail/zh/canncommercial/850/softwareinst/instg/instg_0005.html?Mode=PmIns&InstallType=local&OS=openEuler)。
- [安装Ascend-cann-toolkit，请参见《CANN 软件安装指南](https://www.hiascend.com/document/detail/zh/canncommercial/850/softwareinst/instg/instg_0000.html?Mode=PmIns&InstallType=local&OS=openEuler)》。
- [若要使用MindStudio Insight进行查看时，需要单独安装MindStudio Insight软件包，具体下载链接请参见“安装与卸载](https://www.hiascend.com/document/detail/zh/mindstudio/830/GUI_baseddevelopmenttool/msascendinsightug/Insight_userguide_0005.html)”。

- **在安装昇腾AI处理器的服务器执行npu-smi info****命令进行查询，获取Chip Name****信息。实际配置值为AscendChip Name，例如Chip Name***取值为xxxyy**，实际配置值为Ascendxxxyy。**当Ascendxxxyy为代码样例路径时，需要配置Ascendxxxyy*。
- 如果需要指令占比饼图（instruction_cycle_consumption.html），则需要安装生成饼图所依赖的Python三方库plotly。
```
pip3 install plotly
```

**父主题：**[算子开发工具快速入门](tools_qucikstart_0006.html)