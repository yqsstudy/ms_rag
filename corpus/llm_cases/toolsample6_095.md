---
title: "模型压缩量化"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_095.html"
date_collected: "2026-05-04"
category: "llm_cases"
original_path: "zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_095.html"
---

# 模型压缩量化

量化可以使模型压缩，减少计算量。

- 昇腾仅支持对Cube算子（MatMul、Conv）的量化。
- [由于量化会插入一些数据转换算子，可能会导致性能劣化，如果需要量化，建议量化后使用AOE等手段进行优化，对比量化前后的性能。AOE方法参考5.6.3.2-ONNX模型调优](toolsample6_084.html)章节。

量化方法包括以下几种：

- [通过ATC进行量化：进行ATC转换时使用--compression_optimize_conf参数，直接得到量化后的OM文件，使用方法详见《ATC离线模型编译工具用户指南](https://www.hiascend.com/document/detail/zh/canncommercial/850/devaids/atctool/atlasatc_16_0031.html)[》的“参数说明](https://www.hiascend.com/document/detail/zh/canncommercial/850/devaids/atctool/atlasatc_16_0039.html)”章节。
- AMCT_ONNX：针对ONNX进行量化，需下载并安装“AMCT（ONNX）”，相当于ATC参数量化的ONNX版本。AMCT工具在CANN软件下载链接中获取，AMCT支持联合量化，在resnet结构上可能会有额外的性能提升。
- [msModelSlim工具：针对ONNX进行量化，CANN包自带工具，无需安装，支持超2G的ONNX模型量化， 使用指导请参考msModelSlim工具](https://gitcode.com/Ascend/msit/tree/master/msmodelslim)。
**父主题：**[优化方法](toolsample6_094.html)