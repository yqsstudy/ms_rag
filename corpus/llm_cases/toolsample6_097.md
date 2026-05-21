---
title: "简化ONNX文件"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_097.html"
date_collected: "2026-05-04"
category: "llm_cases"
original_path: "zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_097.html"
---

# 简化ONNX文件

ONNX Simplifier是一款开源工具，可以简化ONNX模型。通过推断整个计算图，用常量输出替换冗余运算符（也称为常量折叠）。

执行以下命令，使用ONNX Simplifier工具。

```
pip install onnx-simplifier
onnxsim -h  #查看参数说明
onnxsim  --overwrite-input-shape="1,3,224,24" efficient.onnx efficient_sim.onnx
```

如图1所示，对导出的ONNX文件进行onnxsim后可以看到，减少了ONNX部分的操作。
**图1**使用ONNX Simplifier工具

**父主题：**[ONNX模型调优](toolsample6_096.html)