---
title: "简介"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/ModelAccuracyAnalyzer/atlasaccuracy_16_0001.html"
date_collected: "2026-05-04"
category: "accuracy_tools"
original_path: "zh/mindstudio/830/T&ITools/ModelAccuracyAnalyzer/atlasaccuracy_16_0001.html"
---

# 简介

相比于业界标杆算子，昇腾自研算子在昇腾AI处理器上的运算结果可能存在差异：

- **模型迁移**：原始模型（基于GPU）在迁移到昇腾环境进行训练或在线推理时，昇腾自研算子的运算结果与业界标杆算子存在差异。
- **模型转换**：ATC工具转换模型时，会对模型进行算子消除、算子融合、算子拆分等优化，这些操作可能会造成昇腾自研算子运算结果与业界标杆算子运算结果的差异。
- **模型兼容**：ATC工具转换的离线模型，由于CANN软件版本迭代、模型版本迭代、模型优化、硬件升级或ATC转换前开启或关闭了算子融合功能，可能会造成升级或优化后的离线模型存在精度下降问题。

为了帮助开发人员快速解决算子精度问题，精度调试工具提供了昇腾自研算子运算结果与业界标杆算子运算结果之间的比对功能。

[有关ATC的详细介绍请参见《ATC离线模型编译工具用户指南](https://www.hiascend.com/document/detail/zh/canncommercial/850/devaids/atctool/atlasatc_16_0031.html)》。

#### 精度比对总体流程

精度比对总体流程如下：

以下流程图描述的是当前工具支持的三类场景：

- [GPU vs Ascend NPU（训练）：表示训练原始模型（基于GPU）迁移到昇腾NPU环境后，二者的精度数据对比。对应章节GPU vs NPU（TensorFlow 1.15训练/在线推理）](atlasaccuracy_16_0005.html#ZH-CN_TOPIC_0000002536023765)。
- [GPU/CPU vs Ascend NPU（推理）：表示推理原始模型（基于GPU/CPU）进行模型转换后，二者的精度数据对比。对应章节GPU vs NPU（TensorFlow离线推理）](atlasaccuracy_16_0013.html#ZH-CN_TOPIC_0000002536143801)[、GPU vs NPU（ONNX离线推理）](atlasaccuracy_16_0019.html#ZH-CN_TOPIC_0000002504183990)[和GPU/CPU vs NPU（Caffe离线推理）](atlasaccuracy_16_0025.html#ZH-CN_TOPIC_0000002504343830)。
- [Ascend NPU vs Ascend NPU（推理）：表示已完成ATC工具转换的离线模型，由于CANN软件版本迭代、模型版本迭代、模型优化、硬件升级或ATC转换前开启或关闭了算子融合功能等情况，对前后两个版本的模型进行精度数据对比。对应章节NPU vs NPU（离线推理）](atlasaccuracy_16_0032.html#ZH-CN_TOPIC_0000002536023775)。
**图1**
精度比对总体流程