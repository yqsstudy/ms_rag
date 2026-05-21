---
title: "比对操作和分析"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/ModelAccuracyAnalyzer/atlasaccuracy_16_0035.html"
date_collected: "2026-05-04"
category: "accuracy_tools"
original_path: "zh/mindstudio/830/T&ITools/ModelAccuracyAnalyzer/atlasaccuracy_16_0035.html"
---

# 比对操作和分析

#### 说明

当指定的比对数据文件大小超过1GB或.json文件大小超过100MB时，比对过程可能耗时较长，系统提示：'The size (%d) of %s more than the XX, it needs more time to run.'。

#### 前提条件

- [请确保完成使用前准备](atlasaccuracy_16_0002.html#ZH-CN_TOPIC_0000002504343822)。
- [根据总体说明](atlasaccuracy_16_0033.html#ZH-CN_TOPIC_0000002536143809)中的场景准备比对文件。

#### 操作步骤

1. 登录CANN工具安装环境。
2. 生成json文件。

  - 使用开启算子融合功能的离线模型生成resnet50_on.json文件。******
```
atc --mode=1 --om=$HOME/module/out/caffe_resnet50_on.om --json=$HOME/module/out/caffe_resnet50/resnet50_on.json
```

  - 使用关闭算子融合功能的离线模型生成resnet50_off.json文件。******
```
atc --mode=1 --om=$HOME/module/out/caffe_resnet50_off.om --json=$HOME/module/out/caffe_resnet50/resnet50_off.json
```


[版本迭代前后精度比对](atlasaccuracy_16_0033.html#ZH-CN_TOPIC_0000002536143809__zh-cn_topic_0000002534483601_section5628111016542)场景跳过此步骤。

3. 进入${INSTALL_DIR}/tools/operator_cmp/compare，${INSTALL_DIR}请替换为CANN软件安装后文件存储路径。以root用户安装为例，则安装后文件存储路径为：/usr/local/Ascend/cann。
4. 执行比对命令。

假设开启和关闭算子融合功能的离线模型在昇腾AI处理器上运行生成dump数据。

数据分别保存在：

  - $HOME/MyApp_mind/resnet50_on
  - $HOME/MyApp_mind/resnet50_off

[版本迭代前后精度比对](atlasaccuracy_16_0033.html#ZH-CN_TOPIC_0000002536143809__zh-cn_topic_0000002534483601_section5628111016542)场景同样是把两份比对数据保存在不同目录下。

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

指定全网层信息文件（即配置-f和-cf参数）
**********
```
python3 msaccucmp.py compare -m $HOME/MyApp_mind/resnet50_on -g $HOME/MyApp_mind/resnet50_off  -f $HOME/module/out/caffe_resnet50/resnet50_on.json -cf $HOME/module/out/caffe_resnet50/resnet50_off.json -out $HOME/MyApp_mind/out
```

或

不指定全网层信息文件（即不配置-f和-cf参数）
******
```
python3 msaccucmp.py compare -m $HOME/MyApp_mind/resnet50_on -g $HOME/MyApp_mind/resnet50_off -out $HOME/MyApp_mind/out
```

[上述命令仅展示当前场景所需参数的示例，若需要配置更多参数，比如已知可能出现精度问题的范围或因大型网络模型输出结果文件数据量过大，通过配置参数来减少输出结果的数据量，请参见命令格式说明](atlasaccuracy_16_0063.html#ZH-CN_TOPIC_0000002536143825)获取更多参数详细介绍。
**表1**整网比对命令行参数说明
**参数名**

**参数说明**

**是否必选**

-m

--my_dump_path

开启算子融合功能的离线模型基于昇腾AI处理器运行生成的数据文件所在目录。

是

-g

--golden_dump_path

关闭算子融合功能的离线模型基于昇腾AI处理器运行生成的数据文件所在目录。

是

-f

--fusion_rule_file

全网层信息文件。使用开启算子融合功能的离线模型通过ATC转换生成的.json文件。

[版本迭代前后精度比对](atlasaccuracy_16_0033.html#ZH-CN_TOPIC_0000002536143809__zh-cn_topic_0000002534483601_section5628111016542)场景无需配置。

否

-cf

--close_fusion_rule_file

全网层信息文件。

使用关闭算子融合功能的离线模型通过ATC转换生成的.json文件。

[版本迭代前后精度比对](atlasaccuracy_16_0033.html#ZH-CN_TOPIC_0000002536143809__zh-cn_topic_0000002534483601_section5628111016542)场景无需配置。

否

-out

--output

比对数据结果存放路径，默认为当前路径。

不建议配置与当前用户不一致的其它用户目录，避免提权风险。

否
|  |  |  |
| --- | --- | --- |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
比对结果如图1所示。**图1**
融合算子精度问题排查比对结果
[以上比对结果字段解释请参见完整比对结果参数说明](atlasaccuracy_16_0064.html#ZH-CN_TOPIC_0000002504184012)。

其中NPUDump表示开启算子融合功能的离线模型的算子名；GroundTruth表示关闭算子融合功能的离线模型的算子名。

5. 比对结果分析。

[请参见比对结果分析](atlasaccuracy_16_0037.html#ZH-CN_TOPIC_0000002504343836)[。对于比对结果中可能存在部分无法比对或异常情况（例如结果中的NaN），请参见比对结果说明](atlasaccuracy_16_0036.html#ZH-CN_TOPIC_0000002504183998)。

**父主题：**[NPU vs NPU（离线推理）](atlasaccuracy_16_0032.html)