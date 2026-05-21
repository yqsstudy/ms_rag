---
title: "精度调试"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/msquickstart/atlasquick_infer_0004.html"
date_collected: "2026-05-04"
category: "quickstart"
original_path: "zh/mindstudio/830/msquickstart/atlasquick_infer_0004.html"
---

# 精度调试

#### 前提条件

- [已参见模型量化](atlasquick_infer_0003.html#ZH-CN_TOPIC_0000002538345651)章节完成模型量化。
- [已参见模型量化章节的1](atlasquick_infer_0003.html#ZH-CN_TOPIC_0000002538345651__zh-cn_topic_0000002502743726_li125721416491)准备好浮点模型。

#### 量化模型dump

1. 执行以下命令，确认量化模型是否可以推理。
******
```
bash ${ATB_SPEED_HOME_PATH}/examples/models/llama3/run_pa.sh ${save_directory} ${max_output_length}
```

其中参数解释如下：

  - **ATB_SPEED_HOME_PATH**：默认路径为“/usr/local/Ascend/atb-models”，在source模型仓中set_env.sh脚本时已配置；
  - **max_output_length**：对话测试中最大输出token数。
执行完命令后，回显信息有如下内容，说明量化模型可以进行推理。
```
1
2
3
```

```
Question[0]: What's deep learning?
Answer[0]:  Deep learning is a subset of machine learning that uses artificial neural networks to analyze data. It's called
Generate[0] token num: (0, 20)

```
|  |  |
| --- | --- |

2. 执行以下命令，对量化模型进行dump，结果保存至用户指定dump数据的输出路径。以下命令中的参数说明请参见表1[。此处以指定dump第二个token为例。如果需要了解更多的参数信息，请参见加速库模型数据dump](https://gitcode.com/ascend/msit/blob/master/msit/docs/llm/工具-DUMP加速库数据使用说明.md)。
********
```
msit llm dump --exec "bash ${ATB_SPEED_HOME_PATH}/examples/models/llama3/run_pa.sh ${save_directory} ${max_output_length}" --type model tensor -er 2,2 -o ${quant_dump_path}
```
**表1**dump参数说明
参数

说明

使用示例

--exec

指定包含ATB的程序执行命令。

命令中不支持重定向字符，如果需要重定向输出，建议将执行命令写入shell脚本，然后启动shell脚本。

--exec "bash run.sh patches/models"

--type

dump类型，默认为['tensor', 'model']。

常用可选项如下：

  - model：模型拓扑信息（默认），当dump类型为model时，layer会跟着model一起dump下来。
  - layer：Operation维度拓扑信息。
  - tensor：tensor数据（默认）。

--type layer tensor

-er, --execute-range

指定dump的token编号范围，区间左右全闭，可以支持多个区间序列，默认为第0个。

请确保输入多区间时的总输入长度不超过500个字符。

-er 2,2

-er 3,5,7,7：代表区间[3,5],[7,7]，也就是第3，第4，第5，第7个token

-o, --output

指定dump数据的输出目录，默认为./。

-o /home/projects/output
|  |  |  |
| --- | --- | --- |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |

3. 量化模型dump成功后，落盘数据目录结构如下。

```
├── {quant_dump_path}/              # 数据保存路径   
│    └── msit_dump_{timestamp}/    # 数据落盘时间戳目录
      │    ├── layer/              # 网络结构子目录
      │    ├── model/              # 模型信息目录
      │    ├── tensors/            # tensor子目录
```

#### 浮点模型dump

1. 执行以下命令，确认浮点模型是否可以推理。
******
```
bash ${ATB_SPEED_HOME_PATH}/examples/models/llama3/run_pa.sh --model_path ${model_path} ${max_output_length}
```

2. 回显信息有如下内容，说明浮点模型可以进行推理。

```
1
2
3
```

```
Question[0]: What's deep learning?
Answer[0]:  Deep learning is a subset of machine learning that uses artificial neural networks to analyze data. It's called
Generate[0] token num: (0, 20)

```
|  |  |
| --- | --- |

3. 执行浮点模型dump，结果保存至用户指定dump数据的输出路径。命令中的参数说明请参见表1。此处以指定dump第二个token为例。
********
```
msit llm dump --exec "bash ${ATB_SPEED_HOME_PATH}/examples/models/llama3/run_pa.sh --model_path ${model_path} ${max_output_length}" --type model tensor -er 2,2 -o ${float_dump_path}
```

4. 浮点模型dump成功后，会在float_dump文件夹下生成msit_dump_{timestamp}文件夹，落盘数据目录结构如下。

```
├── {float_dump_path}/              # 数据保存路径   
│    └── msit_dump_{timestamp}/    # 数据落盘时间戳目录
      │    ├── layer/              # 网络结构子目录
      │    ├── model/              # 模型信息目录
      │    ├── tensors/            # tensor子目录
```

#### 精度比对

1. 执行以下命令，对量化模型dump后的结果文件和浮点模型dump后的结果文件进行精度比对。命令中参数解释如表2所示。
******************
```
msit llm compare -gp 
${float_dump_path}/msit_dump_{timestamp}/tensors/{device_id}_{process_id}/2/
-mp ${quant_dump_path}/msit_dump_{timestamp}/tensors/{device_id}_{process_id}/2/ -o ${compare_result_dir}
```
**表2**compare参数解释
参数

说明

-gp

用于指定标杆数据路径的参数，即浮点模型dump数据所在目录。

-mp

用于指定待比对的数据路径的参数，即量化模型dump数据所在目录。

-o

用于指定比对结果保存路径。
|  |  |
| --- | --- |
|  |  |
|  |  |
|  |  |

2. [精度比对回显信息如下，比对结果文件中的参数说明可参见精度比对结果参数说明](https://gitcode.com/ascend/msit/blob/master/msit/docs/llm/精度比对结果参数说明.md)，做进一步分析。

```
1
2
3
4
5
```

```
msit_llm_logger - INFO - golden_layer_type: Prefill_layer
msit_llm_logger - INFO - my_layer_type: Prefill_layer
msit_llm_logger - INFO - golden_layer_type: Decoder_layer
msit_llm_logger - INFO - my_layer_type: Decoder_layer
msit_llm_logger - INFO - Saved comparing results: ./msit_cmp_report_{timestamp}.csv

```
|  |  |
| --- | --- |

**父主题：**[模型推理](atlasquick_infer_0002.html)