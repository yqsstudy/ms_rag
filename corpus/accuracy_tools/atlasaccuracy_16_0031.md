---
title: "比对操作和分析"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/ModelAccuracyAnalyzer/atlasaccuracy_16_0031.html"
date_collected: "2026-05-04"
category: "accuracy_tools"
original_path: "zh/mindstudio/830/T&ITools/ModelAccuracyAnalyzer/atlasaccuracy_16_0031.html"
---

# 比对操作和分析

#### 说明

- 本节涉及的.json文件、目录等名称均为举例，请根据实际环境替换。其中，-out指定的结果存放路径，需确保操作用户具有读写权限。
- 如果执行过程中报“MemoryError”，则表示数据量过大导致了内存溢出，请将NPU的dump数据文件拆分到多个目录后，再逐一进行比对。
- 当指定的比对数据文件大小超过1GB或.json文件大小超过100MB时，比对过程可能耗时较长，系统提示：'The size (%d) of %s more than the XX, it needs more time to run.'。
- 使用量化离线模型在昇腾AI处理器上运行生成的dump数据作为待比对数据时，由于量化与反量化算子之间存在影响精度的中间算子，在比对时会与源数据产生较大的精度损失，所以精度比对时会过滤掉中间算子进行比对，此时输出的结果将不包含整网的所有算子。

#### 前提条件

- [请确保完成使用前准备](atlasaccuracy_16_0002.html#ZH-CN_TOPIC_0000002504343822)。
- [根据总体说明](atlasaccuracy_16_0026.html#ZH-CN_TOPIC_0000002536023773)中的场景准备比对文件。

#### 操作步骤

1. 登录CANN工具安装环境。
2. 进入${INSTALL_DIR}/tools/operator_cmp/compare，${INSTALL_DIR}请替换为CANN软件安装后文件存储路径。以root用户安装为例，则安装后文件存储路径为：/usr/local/Ascend/cann。
3. 执行比对命令。

**由于dump和npy比对数据文件是由多个文件组成，故下文操作步骤中-m****和-g***参数须指定数据文件所在的父目录。如：$HOME/MyApp/resnet50，**其中resnet50*文件夹下直接保存比对数据文件。

目录结构示例如下：

```
1
2
3
4
5
6
```

```
root@xxx:$HOME/MyApp/resnet50# tree
.
├── BatchMatMul.bert_encoder_layer_0_attention_self_MatMul_1.24.1614717261785536
├── BatchMatMul.bert_encoder_layer_0_attention_self_MatMul.21.1614717261768864
├── BatchMatMul.bert_encoder_layer_10_attention_self_MatMul_1.235.1614717263664916
# 仅为示例，此处省略剩余文件名。

```
|  |  |
| --- | --- |

  - 非量化原始模型 vs 非量化离线模型、非量化原始模型 vs 量化离线模型、量化原始模型 vs 量化离线模型********
```
python3 msaccucmp.py compare -m $HOME/MyApp_mind/resnet50 -g $HOME/Standard_caffe/resnet50 -f $HOME/data/resnet50.json -out $HOME/result -advisor
```

  - 非量化原始模型 vs 量化原始模型********
```
python3 msaccucmp.py compare -m $HOME/MyApp_mind/resnet50 -g $HOME/Standard_caffe/resnet50 -q $HOME/data/resnet50_quant.json -out $HOME/result -advisor
```


  - [上述命令仅展示当前场景所需参数的示例，若需要配置更多参数，比如已知可能出现精度问题的范围或因大型网络模型输出结果文件数据量过大，通过配置参数来减少输出结果的数据量，请参见命令格式说明](atlasaccuracy_16_0063.html#ZH-CN_TOPIC_0000002536143825)获取更多参数详细介绍。
  - 需要安装pandas 1.3或更高版本依赖，否则无法执行-advisor参数输出专家建议。
**表1**整网比对命令行参数说明
**参数名**

**参数说明**

**是否必选**

-m

--my_dump_path

基于昇腾AI处理器运行生成的数据文件所在目录。

是

-g

--golden_dump_path

基于GPU/CPU运行生成的原始网络数据文件所在目录。

是

-f

--fusion_rule_file

全网层信息文件。

通过ATC转换.om模型文件生成的.json文件，文件包含整网算子的映射关系，用于精度比对时算子匹配。

Caffe非量化原始模型 vs 量化离线模型场景时，与-q参数二选一；Caffe非量化原始模型 vs 量化原始模型场景时，仅使用-q参数。

否

-q

--quant_fusion_rule_file

量化信息文件。

通过AMCT量化生成的量化信息文件（*.json），文件包含整网量化算子映射关系，用于精度比对时算子匹配。

Caffe非量化原始模型 vs 量化离线模型场景时，与-f参数二选一；Caffe非量化原始模型 vs 量化原始模型场景时，仅使用本参数。

否

-out

--output

比对数据结果存放路径，默认为当前路径。

不建议配置与当前用户不一致的其它用户目录，避免提权风险。

否

-advisor

[在Tensor比对结束后，针对比对结果进行数据分析，给出专家建议。详情请参见比对结果专家建议](atlasaccuracy_16_0039.html#ZH-CN_TOPIC_0000002536143813)

否
|  |  |  |
| --- | --- | --- |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |

比对结果如图1所示。
**图1**
比对结果示例
[以上比对结果字段解释请参见完整比对结果参数说明](atlasaccuracy_16_0064.html#ZH-CN_TOPIC_0000002504184012)。

4. 比对结果分析。

[请参见比对结果分析](atlasaccuracy_16_0037.html#ZH-CN_TOPIC_0000002504343836)[。对于比对结果中可能存在部分无法比对或异常情况（例如结果中的NaN），请参见比对结果说明](atlasaccuracy_16_0036.html#ZH-CN_TOPIC_0000002504183998)。

**父主题：**[GPU/CPU vs NPU（Caffe离线推理）](atlasaccuracy_16_0025.html)