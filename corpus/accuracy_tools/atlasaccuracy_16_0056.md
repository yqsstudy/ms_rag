---
title: "GPU/NPU映射表获取"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/ModelAccuracyAnalyzer/atlasaccuracy_16_0056.html"
date_collected: "2026-05-04"
category: "accuracy_tools"
original_path: "zh/mindstudio/830/T&ITools/ModelAccuracyAnalyzer/atlasaccuracy_16_0056.html"
---

# GPU/NPU映射表获取

#### 说明

本节涉及的.json文件、目录等名称均为举例，请根据实际环境替换。其中，-out指定的结果存放路径，需确保操作用户具有读写权限。

#### 操作步骤

1. 以HwHiAiUser用户登录开发环境。
2. 生成json文件。
******
```
atc --mode=1 --om=$HOME/data/resnet50.om --json=$HOME/data/resnet50.json
```

3. 进入${INSTALL_DIR}/tools/operator_cmp/compare，${INSTALL_DIR}请替换为CANN软件安装后文件存储路径。以root用户安装为例，则安装后文件存储路径为：/usr/local/Ascend/cann。
4. 执行获取GPU/NPU的映射表命令。

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

********
```
python3 msaccucmp.py compare -m $HOME/MyApp_mind/resnet50 -g $HOME/Standard_caffe/resnet50 -f $HOME/data/resnet50.json -out $HOME/result -map
```

输出结果为mapping_*.csv文件内容如图1所示。
**图1**
GPU/NPU的映射表**表1**输出参数说明
参数

说明

Index

算子的ID。

OpType

算子类型。指定-f，-cf或-q参数时获取算子类型。

NPUDump

表示基于昇腾AI处理器运行生成的dump数据的算子名。

GroundTruth

表示基于GPU/CPU运行生成的npy或dump数据的算子名。

TensorIndex

表示基于昇腾AI处理器运行生成的dump数据的算子的input ID和output ID。

NPUDumpPath

表示基于昇腾AI处理器运行生成的dump文件路径。

GroundTruthPath

表示基于GPU/CPU运行生成的npy或dump文件路径。
|  |  |
| --- | --- |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |

**父主题：**[扩展功能](atlasaccuracy_16_0051.html)