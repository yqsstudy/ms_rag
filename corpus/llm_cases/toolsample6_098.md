---
title: "ATC调优"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_098.html"
date_collected: "2026-05-04"
category: "llm_cases"
original_path: "zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_098.html"
---

# ATC调优

ATC工具运行命令参考如下：例：
********
```
atc --framework=5 \
--model=models/vit-b-16.img.fp32.bs${bs}.opt.onnx \
--output=models/vit-b-16.img.bs${bs} \
--input_format=NCHW \
--input_shape="image:${bs},3,224,224" \
--soc_version=Ascend${chip_name} \
--log=error \
--optypelist_for_implmode="Sigmoid" \
--op_select_implmode=high_performance \
--enable_small_channel \
--insert_op_conf=./insert_op.cfg
```

命令中的参数说明如表1[所示，更多参数说明可参考《ATC离线模型编译工具用户指南](https://www.hiascend.com/document/detail/zh/canncommercial/850/devaids/atctool/atlasatc_16_0031.html)》。
**表1**参数说明
参数

说明

--model

ONNX模型文件。

--framework

5代表ONNX模型。

--output

输出的OM模型。

--input_format

输入数据的格式。

--input_shape

输入数据的Shape。

--log

日志级别。

--soc_version

处理器型号。

--optypelist_for_implmode

指定算子。

--op_select_implmode

选择高性能/高精度模式，与--optypelist_for_implmode配合使用。

--enable_small_channel

与--insert_op_conf配合使用。

--fusion_switch_file

关闭/打开部分融合规则。
|  |  |
| --- | --- |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
**父主题：**[ONNX模型调优](toolsample6_096.html)