---
title: "结果文件说明"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/ModelAccuracyAnalyzer/atlasaccuracy_16_0050.html"
date_collected: "2026-05-04"
category: "accuracy_tools"
original_path: "zh/mindstudio/830/T&ITools/ModelAccuracyAnalyzer/atlasaccuracy_16_0050.html"
---

# 结果文件说明

[单算子比对执行比对操作](atlasaccuracy_16_0049.html#ZH-CN_TOPIC_0000002504343842)，默认比对指定算子数据的绝对误差和相对误差，根据指定比对算子的输入或输出数据以及设置的输出文件形式生成比对结果文件如表1。
**表1**结果文件形式
结果文件输出条件

结果文件

比对输入数据、默认生成前20条数据

--input_tensor

单算子比对概要结果：{op_name}_input_{index}_summary.txt

单算子比对完整结果：{op_name}_input_{index}_{file_index}.csv

单算子比对Top20结果：

- 绝对误差：{op_name}_input_{index}_absolute_error_topn.csv
- 相对误差：{op_name}_input_{index}_relative_error_topn.csv

比对输出数据、默认生成前20条数据

--output_tensor

单算子比对概要结果：{op_name}_output_{index}_summary.txt

单算子比对完整结果：{op_name}_output_{index}_{file_index}.csv

单算子比对Top20结果：

- 绝对误差：{op_name}_output_{index}_absolute_error_topn.csv
- 相对误差：{op_name}_output_{index}_relative_error_topn.csv

比对输入数据、生成前n条数据

--input_tensor、--topn

单算子比对概要结果：{op_name}_input_{index}_summary.txt

单算子比对完整结果：{op_name}_input_{index}_{file_index}.csv

单算子比对TopN结果：

- 绝对误差：{op_name}_input_{index}_absolute_error_topn.csv
- 相对误差：{op_name}_input_{index}_relative_error_topn.csv

比对输出数据、生成前n条数据

--output_tensor、--topn

单算子比对概要结果：{op_name}_output_{index}_summary.txt

单算子比对完整结果：{op_name}_output_{index}_{file_index}.csv

单算子比对TopN结果：

- 绝对误差：{op_name}_output_{index}_absolute_error_topn.csv
- 相对误差：{op_name}_output_{index}_relative_error_topn.csv

比对输入数据、不生成完整比对数据、默认生成前20条数据

--input_tensor、--ignore_single_op_result

单算子比对概要结果：{op_name}_input_{index}_summary.txt

单算子比对Top20结果：

- 绝对误差：{op_name}_input_{index}_absolute_error_topn.csv
- 相对误差：{op_name}_input_{index}_relative_error_topn.csv

比对输出数据、不生成完整比对数据、默认生成前20条数据

--output_tensor、--ignore_single_op_result

单算子比对概要结果：{op_name}_output_{index}_summary.txt

单算子比对Top20结果：

- 绝对误差：{op_name}_output_{index}_absolute_error_topn.csv
- 相对误差：{op_name}_output_{index}_relative_error_topn.csv

比对输入数据、配置单个csv文件包含最大文件条数、默认生成前20条数据

--input_tensor、--max_line

单算子比对概要结果：{op_name}_input_{index}_summary.txt

单算子比对拆分结果：{op_name}_input_{index}_{file_index}.csv

单算子比对Top20结果：

- 绝对误差：{op_name}_input_{index}_absolute_error_topn.csv
- 相对误差：{op_name}_input_{index}_relative_error_topn.csv

比对输出数据、配置单个csv文件包含最大文件条数、默认生成前20条数据

--output_tensor、--max_line

单算子比对概要结果：{op_name}_output_{index}_summary.txt

单算子比对拆分结果：{op_name}_output_{index}_{file_index}.csv

单算子比对Top20结果：

- 绝对误差：{op_name}_output_{index}_absolute_error_topn.csv
- 相对误差：{op_name}_output_{index}_relative_error_topn.csv

注1：当算子名称{op_name}过长时，将自动转换为比对算子所在的dump文件名，增加输出转换后的结果文件与实际结果文件（超长算子名未转换）的映射关系文件“simple_op_mapping.csv”。

注2：file_index为输出结果csv文件的编号，默认情况下为0，当配置--max_line时，则取值为(n-1)*max_line，n为从1开始的正整数。

[注3：以上各参数详细介绍请参见命令格式说明](atlasaccuracy_16_0063.html#ZH-CN_TOPIC_0000002536143825)。
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
**父主题：**[单算子比对](atlasaccuracy_16_0047.html)