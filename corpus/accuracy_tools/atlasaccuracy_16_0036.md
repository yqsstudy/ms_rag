---
title: "比对结果说明"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/ModelAccuracyAnalyzer/atlasaccuracy_16_0036.html"
date_collected: "2026-05-04"
category: "accuracy_tools"
original_path: "zh/mindstudio/830/T&ITools/ModelAccuracyAnalyzer/atlasaccuracy_16_0036.html"
---

# 比对结果说明

本节内容主要说明对于比对结果中可能存在部分无法比对或异常情况（比如结果中的NaN）。

- 对于Caffe、TensorFlow模型，若不是相同模型的数据，但模型中有相同的算子名称，也可以进行比对，但结果数据只显示匹配到的相同算子的比对结果，该场景不进行分析。
- 如果在图编译过程中，原图的算子发生了融合，导致算子的output在编译后的模型中找不到对应的output时，该算子无法进行比对。
- 如果在图编译阶段对图做了结构性修改（如stride切分、L1 fusion、L2 fusion）的场景，会造成算子的input或output无法比对。
- 如果比对数据两边相同算子有dump数据，但算子的Shape不一致（离线模型算子Shape变小）或Format不支持转换，该算子无法进行比对。
- 量化模型里经过量化处理的算子无法比对，必须是反量化的输出才能比对。例如，量化模型里AscendQuant算子的output无法比对。
- 针对FastRCNN网络场景，ProposalD算子及之后的算子，算子精度不达标属于正常情况，最终结果以FSRDetectionOutput算子的比对结果精度为准。
- 当模型转换对输入数据做了额外的预处理，造成原始模型的输入与离线模型的data算子输入格式不同时（比如AIPP场景下data输入为YUV），data算子比对结果异常、不具备参考意义。
- 如果比对数据两边相同算子有多个input且input顺序不一致，会导致该算子的input的比对结果不可信。
- 如果没有关闭对应的融合规则，会使得量化算子与之前的算子进行融合，导致该算子的output的比对结果不可信。