---
title: "数据格式要求"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/ModelAccuracyAnalyzer/atlasaccuracy_16_0062.html"
date_collected: "2026-05-04"
category: "accuracy_tools"
original_path: "zh/mindstudio/830/T&ITools/ModelAccuracyAnalyzer/atlasaccuracy_16_0062.html"
---

# 数据格式要求

**msaccucmp.py**脚本精度比对工具支持多种比对方式，因此dump、npy文件命名需满足以下要求：
**表1**数据文件命名规则
数据类型

数据命名格式

备注

非量化离线模型在昇腾AI处理器上运行生成的dump数据文件

*{op_type}.{op_name}.{task_id}.{stream_id}.{timestamp}*

当前包含如下三种文件名格式：

- *{op_type}.{op_name}.{task_id}.{stream_id}.{timestamp}*
- *{op_type}.{op_name_lxsliceN}.({stream_id}.){task_id}.{timestamp}.{task_type}.{context_id}.{thread_id}.{device_id}*
- *{op_type}.{op_name}.({stream_id}.){task_id}.{timestamp}.{task_type}.{context_id}.{thread_id}.{device_id}*

命名格式说明：

- op_type（算子类型）、op_name（算子名）对应的名称需满足“A-Za-z0-9_-”正则表达式规则。
- timestamp为16位时间戳。
- task_id（任务ID）、stream_id（Stream ID）、output_index（第N个输出）、task_type（任务类型）、context_id（Context ID）、thread_id（线程ID）、device_id（运行卡的Device ID）为0~9数字组成。

如果op_type、op_name出现了“.”、“/”、“\”、空格时，转换为下划线表示。

量化离线模型在昇腾AI处理器上运行生成的dump数据文件

npy文件（Caffe、TensorFlow或ONNX）

*{op_name}.{output_index}.{timestamp}*.npy
|  |  |  |
| --- | --- | --- |
|  |  |  |
|  |  |  |
|  |  |  |
**父主题：**[附录](atlasaccuracy_16_0061.html)