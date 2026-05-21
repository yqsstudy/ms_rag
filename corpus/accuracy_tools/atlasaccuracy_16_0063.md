---
title: "命令格式说明"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/ModelAccuracyAnalyzer/atlasaccuracy_16_0063.html"
date_collected: "2026-05-04"
category: "accuracy_tools"
original_path: "zh/mindstudio/830/T&ITools/ModelAccuracyAnalyzer/atlasaccuracy_16_0063.html"
---

# 命令格式说明

#### 通用参数

精度比对命令行格式如下：

```
python3 msaccucmp.py compare -m <my_dump_path> -g <golden_dump_path> [-f <fusion_rule_file>] [-cf <close_fusion_rule_file>] [-q <quant_fusion_rule_file>] [-out <output>] [-map] [-c <custom_script_path>] [-alg <algorithm>] [-v <version>] [-r <range>] [-overflow_detection] [-max] [-advisor]
```

命令行参数说明如表1所示。
**表1**精度比对命令行参数说明
**参数名**

**参数说明**

**是否必选**

-m

--my_dump_path

基于昇腾AI处理器运行生成的数据文件所在目录。

*由于dump数据文件是多个二进制文件，故须指定dump数据文件所在的父目录。如：$HOME/MyApp_mind/resnet50，**其中resnet50*文件夹下直接保存dump数据文件。

训练场景下：

- 支持TensorFlow为原始训练网络的比对。
- 单个数据文件比对时，需指定数据文件所在的具体目录。
- **支持多个dump数据文件的批量比对，可指定固定路径为dump_path/time/****，仅支持TensorFlow为原始训练网络的比对。指定的路径下可以存放多个dump数据文件，但要求每个dump数据文件拥有唯一路径，且路径命名规则为dump_path/time/device_id/model_name/model_id/dump_step/dump文件。**

是

-g

--golden_dump_path

基于GPU/CPU运行生成的原始网络数据文件所在目录。

*由于npy文件是多个文件，故须指定npy文件所在的父目录。如：$HOME/Standard_caffe/resnet50******，**其中resnet50*文件夹下直接保存npy数据文件。

当指定-cf参数时，该参数指定的就是模型转换关闭算子融合功能下dump数据文件的目录。

是

-f

--fusion_rule_file

全网层信息文件。

推理场景下：

- 通过使用ATC转换.om模型文件生成的json文件，文件包含整网算子的映射关系。
- 该参数指定的是默认开启算子融合功能情况下进行模型转换时生成的json文件；指定关闭算子融合功能情况下进行模型转换时生成的json文件使用-cf参数。

训练场景下：

- 通过使用ATC转换.txt图文件生成的json文件。
- 单个数据文件比对时，该参数需指定具体的json文件；批量比对时，该参数可指定为多个json文件所在的目录。

否

-cf

--close_fusion_rule_file

全网层信息文件（通过使用ATC转换.om模型文件生成的json文件，文件包含关闭算子融合功能情况下整网算子的映射关系）。

[本参数详细使用指导请参见比对操作和分析](atlasaccuracy_16_0035.html#ZH-CN_TOPIC_0000002536143811)。

仅推理场景支持本参数。

否

-q

--quant_fusion_rule_file

量化信息文件（昇腾模型压缩输出的json文件）。

通过AMCT量化生成的量化信息文件（*.json），文件包含整网量化算子映射关系，用于精度比对时算子匹配。

Caffe非量化原始模型 vs 量化离线模型场景时，与-f参数二选一；Caffe非量化原始模型 vs 量化原始模型场景时，仅使用本参数。

仅推理场景支持本参数。

否

-out

--output

比对数据结果存放路径，默认为当前路径。

不建议配置与当前用户不一致的其它用户目录，避免提权风险。

训练场景下：

- 单个数据文件比对时，结果文件名格式为result_{timestamp}.csv。
- 多个数据文件比对时，结果文件名格式为{device_id}_{model_name}_{dump_step}_result_{timestamp}.csv，批量比对将生成多个csv结果文件。

否

-map

--mapping

输出GPU/NPU的映射表。

[一般情况下GPU/NPU的映射表需要在完成精度比对之后，才能从csv中获取。本参数实现在精度比对前，直接提取GPU/NPU的映射表。建议在比对数据量太大，需要提前获取GPU/NPU的映射表的场景下使用。详细操作请参见GPU/NPU映射表获取](atlasaccuracy_16_0056.html#ZH-CN_TOPIC_0000002504184008)。

否

-c

--custom_script_path

用户自定义脚本文件存放路径，包括自定义算法.py文件和自定义Format转换.py文件，需指定到脚本目录的上一层目录。指定本参数时判断是否存在以下文件目录：

- [存在自定义算法.py文件目录，目录格式为“algorithm”，则读取“algorithm”目录下的自定义算法.py文件，生成自定义算法，可通过-alg参数指定为比对算法。自定义算法.py文件相关要求参见自定义算法.py文件准备](atlasaccuracy_16_0057.html#ZH-CN_TOPIC_0000002504343846)。
- [存在自定义Format转换.py文件目录，目录格式为“format_convert”，则读取“format_convert”目录下的自定义Format转换.py文件。自定义Format转换.py文件相关要求参见准备自定义Format转换.py文件](atlasaccuracy_16_0054.html#ZH-CN_TOPIC_0000002536023787__zh-cn_topic_0000002534483563_zh-cn_topic_0244646216_section6833162804213)。

不建议调用与当前用户不一致的其它用户目录下的自定义脚本文件，避免提权风险。

否

-alg

--algorithm

比对算法维度，取值为：

- 0：CosineSimilarity，表示余弦相似度算法。
- 1：MaxAbsoluteError，表示最大绝对误差算法。
- 2：AccumulatedRelativeError，表示累积相对误差算法。
- 3：RelativeEuclideanDistance，表示欧氏相对距离算法。
- 4：KullbackLeiblerDivergence，表示KL散度算法。
- 5：StandardDeviation，表示标准差算法。
- 6：MeanAbsoluteError，表示平均绝对误差。
- 7：RootMeanSquareError，表示均方根误差。
- 8：MaxRelativeError，表示最大相对误差。
- 9：MeanRelativeError，表示平均相对误差。
- all：比对全部算法（包含自定义和内置算法），all为默认值。
- 自定义算法名（algorithm_name）。具体算法名由自定义算法文件确定，例如自定义算法文件名为alg_RelativeError.py，则自定义算法名为RelativeError。须同时配置-c参数。

可多选，配置格式为各取值间用逗号分隔，可配置为数字或算法名，例如0,1,2,RelativeError。

若只选择比对部分维度，则比对结果同样只展示对应维度。

否

-a

--algorithm_options

**比对算法的高级选项，可为指定的算法设置参数，指定的算法必须是-alg****参数的内置算法或者-c**参数的自定义算法，被本参数设置后的算法以本参数设置的值执行运算。

[输入格式为：算法名:参数名=值,参数名=值;算法名:参数名=值,参数名=值。参数之间是逗号分隔，不同算法是分号分隔，例如："CosineSimilarity:max=1,min=0;aa:max=1,min=0"。其中算法名与-c参数自定义算法.py文件的algorithm_name（参见自定义算法.py文件准备](atlasaccuracy_16_0057.html#ZH-CN_TOPIC_0000002504343846)）一致。

否

-v

*--version*

dump文件类型，1代表protobuf序列化后的数据文件，2代表自定义格式的数据文件。默认取2。

否

-r

--range

设定算子比对范围。配置方式如下：

- start：第一个比对的算子，取值范围为[1, 参与计算的算子个数]，默认值为1。
- end：最后一个比对的算子，取值范围为-1或[start, 参与计算的算子个数]，默认值为-1（动态获取网络模型中最后一个参与计算的算子）。
- step：第start+step*n个比对的算子，step取值范围为[1, 参与计算的算子个数)，默认值为1，n为从1开始的正整数。

配置格式为：“start,end,step”。比如：-r 1,101,20，表示算子1,21,41,61,81,101的Tensor参与比对。

不配置本参数时，比对网络模型中的所有参与计算的算子。

Caffe非量化原始模型 vs 量化原始模型和NPU vs NPU精度比对场景不支持配置本参数。

须先配置-f或-cf参数指定离线模型全网层信息文件。

-s参数与-r参数二者只能选择一个配置。

否

-s

--select

设定算子比对范围。通过指定算子的索引（网络模型中算子的ID）来选择需要比对的算子，格式为：-s 1,2,3（数值之间以逗号隔开，取值与网络模型中算子的ID有关）。

须先配置-f或-cf参数指定离线模型全网层信息文件。

-s参数与-r参数二者只能选择一个配置。

否

-max

--max_cmp_size

设置每个dump数据比对的最大字节数，用于精度比对过程提速，默认0（表示全量比对），单位Byte。当模型中算子的输出存在较大Shape时、比对过于耗时，可以尝试配置。

否

-overflow_detection

整网算子溢出检测。进行整网比对时可检测溢出算子。

默认未开启算子溢出检测。

当算子的Tensor数据类型是FP16时，tensor中的任意一个数值的绝对值 >= 65504，认为算子溢出。

Caffe非量化原始模型 vs 量化原始模型场景配置本参数不生效。

否

-advisor

在Tensor比对结束后，针对比对结果进行数据分析，给出专家建议。

否
|  |  |  |
| --- | --- | --- |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |

#### 单算子比对

单算子比对命令行格式如下:

```
python3 msaccucmp.py compare -m <my_dump_path> -g <golden_dump_path> [-f <fusion_rule_file>] [-cf <close_fusion_rule_file>] [-q <quant_fusion_rule_file>] [-out <output>] [-op <op_name>] [-o <output_tensor>] [-i <input_tensor>] [-c <custom_script_path>] [-v <version>] [-n <topn>] [--ignore_single_op_result] [-ml <max_line>] [-overflow_detection]
```

命令行参数说明如表2所示。
**表2**单算子比对命令行参数说明
**参数名**

**参数说明**

是否必选

-op

--op_name

单算子比对的算子名。输入待比对算子名，算子名获取方式有：

- 推理场景下：
  - 从.om模型中获取。
  - 从使用ATC转换.om模型文件生成的json文件中获取。
  - 从整网比对结果文件中的NPUDump字段获取。

- 训练场景下：
  - 直接从训练模型中获取。
  - 从计算图文件（*.txt）中获取。
  - 从整网比对结果文件中的NPUDump字段获取。

是

-o

--output_tensor

比对指定Index的output数据。

*配置格式：-o Index**，其中Index**可以从整网比对结果文件中的TensorIndex字段的output取值获取，例如TensorIndex为trans_Cast_0:input:0，则Index*为0。

当-o与-i均未配置时，默认比对output数据的Index为0的数据。

配置-op时有效，与-i参数互斥。

否

-i

--input_tensor

比对指定Index的input数据。

*配置格式：-i Index**，其中Index**可以从整网比对结果文件中的TensorIndex字段的input取值获取，例如TensorIndex为trans_Cast_0:input:0，则Index*为0。

配置-op时有效，与-o参数互斥。

否

-n

--topn

仅展示绝对误差和相对误差的前n条数据，比对完成后打印并生成csv结果文件，取值范围为[1,10000]，默认值为20。配置-op时有效。

生成的csv结果文件名分别为：

- 绝对误差：{op_name}_{input/output}_{index}_absolute_error_topn.csv
- 相对误差：{op_name}_{input/output}_{index}_relative_error_topn.csv

否

--ignore_single_op_result

csv结果文件中不生成单算子比对的完整比对数据，即不生成完整比对结果的csv文件。配置-op时有效。

不配置本参数时，生成完整比对结果。

否

-ml

--max_line

单算子比对时生成的单个csv文件所包含最大的文件条数，取值范围为[10000,1000000]，默认值为1000000。

文件中单算子的比对结果数据条数较大时，配置本参数可以将csv文件拆分为多个文件。比如数据条数为100000条，配置本参数为10000，那么比对结果则输出10个csv文件。

配置-op时有效，但配置--ignore_single_op_result时，本参数不生效。

否
|  |  |  |
| --- | --- | --- |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
**父主题：**[附录](atlasaccuracy_16_0061.html)