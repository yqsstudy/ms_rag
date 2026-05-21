---
title: "输出结果和优化建议"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/ModelAccuracyAnalyzer/atlasaccuracy_16_0044.html"
date_collected: "2026-05-04"
category: "accuracy_tools"
original_path: "zh/mindstudio/830/T&ITools/ModelAccuracyAnalyzer/atlasaccuracy_16_0044.html"
---

# 输出结果和优化建议

#### Float16溢出检测

针对比对数据中数据类型为Float16的数据，进行溢出检测。如果存在溢出数据，输出专家建议。

**场景限制**：量化原始模型的npy文件（Caffe）与非量化原始模型的npy文件（Caffe）的比对场景不支持溢出检测分析。

需在进行精度比对时指定-overflow_detection参数。

**比对结果**：



算子ID为228的数据，存在Float16数据溢出。

**专家系统分析结果**：

Detection Type: FP16 overflow

Operator Index: 228

Expert Advice: Float16 data overflow occurs. Rectify the fault and perform comparison again.

检测类型：Float16溢出检测

Operator Index：228

专家建议：存在Float16数据溢出，请修正溢出问题，再进行比对。

#### 输入不一致检测

针对整网的输入数据进行检测，主要判断整网两批待比对数据的输入data是否一致。如果存在不一致问题（余弦相似度<0.99），输出专家建议。

**比对结果**：



算子ID为0的数据，输入数据为Input_1，其余弦相似度小于0.99，因此认为此次比对，输入或数据预处理存在问题。

**专家系统分析结果**：

Detection Type: Input inconsistent

Operator Index: 0

Expert Advice: The input data of NPUDump is inconsistent with that of GroundTruth. Use the same data or check the data preprocessing process.

检测类型：输入不一致检测

Operator Index：0

专家建议：NPUDump和GroundTruth的输入数据不一致，请使用相同数据或者检查数据预处理流程。

#### 整网一致性检测（问题节点检测）

判断整网比对结果中，是否某层小于阈值，该层后续数据均小于阈值或最后一层小于阈值（余弦相似度<0.99），输出量化误差修正建议。

**比对结果**：



算子ID为1174的数据，余弦相似度小于0.99，且后续余弦相似度均小于0.99，判断问题节点存在精度问题。

**专家系统分析结果**：

检测类型：整网一致性检测

Operator Index：1174

[专家建议：部分张量精度较低，且导致最终结果精度不达标；很可能由量化造成，请进行数据校准或者您可以获取日志后单击Link](https://www.hiascend.com/support)联系技术支持。

#### 整网一致性检测（单点误差检测）

判断整网比对结果中，是否某层小于阈值（余弦相似度<0.99），但最终结果符合精度要求，输出专家建议。

**比对结果**：



算子ID为195的数据，余弦相似度小于0.99，但最后一层数据符合精度要求，判断为单点误差。

**专家系统分析结果**：

检测类型：整网一致性检测

Operator Index：195

[专家建议：部分张量精度较低，但最终结果精度达标，可能由内部优化导致，请忽略或您可以获取日志后单击Link](https://www.hiascend.com/support)联系技术支持。

#### 整网一致性检测（一致性检测）

比对结果中的所有数据均符合精度要求，输出专家建议。

**比对结果**：



所有数据均符合精度要求，判断模型符合精度要求。

**专家系统分析结果**：

Detection Type: global consistency

Operator Index: NA

Expert Advice: All data in the comparison result meets the accuracy requirements.

If data accuracy of the model is still not up to standard in practical application, please check the post-processing process of model outputs.

检测类型：整网一致性检测

Operator Index：NA

专家建议：比对结果中的所有数据均符合精度要求。

如果模型实际应用中，精度依旧不达标，请排查输出数据的后处理流程。
**父主题：**[比对结果专家建议](atlasaccuracy_16_0039.html)