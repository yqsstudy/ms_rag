---
title: "比对数据说明"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/ModelAccuracyAnalyzer/atlasaccuracy_16_0073.html"
date_collected: "2026-05-04"
category: "accuracy_tools"
original_path: "zh/mindstudio/830/T&ITools/ModelAccuracyAnalyzer/atlasaccuracy_16_0073.html"
---

# 比对数据说明

执行Tensor比对前，请按照表1要求准备好比对数据。

My Output离线模型文件与量化融合规则文件使用场景说明：

- 离线模型文件：使用昇腾AI处理器运行生成的dump数据与Ground Truth比对，选择该模型文件。
- 量化融合规则文件：只要涉及量化与非量化数据比对，则必须选择该文件。
**表1**Tensor比对前数据准备
序号

待比对数据

（My Output）

标准数据

（Ground Truth）

模型文件/融合规则文件

1

非量化离线模型在昇腾AI处理器上运行生成的dump数据

非量化原始模型的npy文件（或dump数据）(Caffe)

非量化离线模型文件（*.om）

2

量化离线模型在昇腾AI处理器上运行生成的dump数据

非量化原始模型的npy文件（或dump数据）(Caffe)

- 量化离线模型文件（*.om）
- 昇腾模型压缩后的量化融合规则文件（json文件）

3

量化原始模型的npy文件（或dump数据）(Caffe)

非量化原始模型的npy文件（或dump数据）(Caffe)

昇腾模型压缩后的量化融合规则文件（json文件）

4

量化离线模型在昇腾AI处理器上运行生成的dump数据

量化原始模型的npy文件（或dump数据）(Caffe)

量化离线模型文件（*.om）

5

非量化离线模型在昇腾AI处理器上运行生成的dump数据

非量化原始模型的npy文件（或dump数据）(TensorFlow)

非量化离线模型文件（*.om）

6

通过昇腾AI处理器运行生成的dump数据

通过昇腾AI处理器运行生成的dump数据

-
|  |  |  |  |
| --- | --- | --- | --- |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
**父主题：**[Tensor比对](atlasaccuracy_16_0071.html)