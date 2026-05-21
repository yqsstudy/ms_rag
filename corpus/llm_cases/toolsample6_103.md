---
title: "msit debug surgeon自动优化ONNX"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_103.html"
date_collected: "2026-05-04"
category: "llm_cases"
original_path: "zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_103.html"
---

# msit debug surgeon自动优化ONNX

[surgeon（自动调优）工具](https://gitcode.com/Ascend/msit/blob/master/msit/docs/debug/surgeon/README.md)使能ONNX模型在昇腾芯片的优化，并提供基于ONNX的改图功能。

#### 使用方法

使用如下命令，进行调优，参数说明如表1所示。

```
msit debug surgeon COMMAND 
```
**表1**参数说明
参数

说明

COMMAND

COMMAND为surgeon工具提供的五个选项：

- list：列举当前支持自动调优的所有知识库。
- evaluate：搜索可以被指定知识库优化的ONNX模型。
- optimize：使用指定的知识库来优化指定的ONNX模型。
- extract：对模型进行子图切分。
- concatenate：对模型进行拼接。
|  |  |
| --- | --- |
|  |  |

[每个子任务下面的可选项和必选项不同。具体使用方法参考msit debug surgeon功能使用指南](https://gitcode.com/Ascend/msit/blob/master/msit/docs/debug/surgeon/README.md)。

#### 优化实例

COMMAND参数取值的实例图1和图2所示。
**图1**
取值为list**图2**
取值为evaluate和optimize
执行前后对比图3所示，可以看出执行后cast算子被消除了。
**图3**
**执行前后对比

父主题：**[优化方法](toolsample6_094.html)