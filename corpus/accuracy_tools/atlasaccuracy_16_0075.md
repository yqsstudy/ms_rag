---
title: "单算子比对"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/ModelAccuracyAnalyzer/atlasaccuracy_16_0075.html"
date_collected: "2026-05-04"
category: "accuracy_tools"
original_path: "zh/mindstudio/830/T&ITools/ModelAccuracyAnalyzer/atlasaccuracy_16_0075.html"
---

# 单算子比对

#### 命令格式说明

Tensor比对命令行格式如下:

```
python3 compare_vector.py -l <LEFT_DUMP_PATH> -r <RIGHT_DUMP_PATH> [-f <FUSION_JSON_FILE_PATH>] [-q <QUANT_FUSION_RULE_FILE_PATH>] -o <OUTPUT_PATH> -d <OP_NAME> [-t <DETAIL_TYPE>] [-i <DETAIL_INDEX>] [-custom <CUSTOM_PATH>]
python3 compare_vector.py -l <LEFT_DUMP_PATH> -r <RIGHT_DUMP_PATH> -f <FUSION_JSON_FILE_PATH> -o <OUTPUT_PATH> -d <OP_NAME> [-t <DETAIL_TYPE>] [-i <DETAIL_INDEX>] [-custom <CUSTOM_PATH>]
```

参数说明如下：

- -l：My Output模型比对数据文件目录。
- -r：Ground Truth模型比对数据文件目录。
- -o：比对数据结果待存储目录。
不建议配置与当前用户不一致的其它用户目录，避免提权风险。

- -f：离线模型的全网层信息文件（通过使用ATC转换.om模型文件生成的json文件或转换.txt图文件生成的json文件）。可选。
- -q：量化融合规则文件。可选。

- -d：待比对的My Output模型单算子层名。
- -t：dump数据的输入输出类型，取值input或output，默认取output。可选。
- -i：My Output模型的算子的input_index或output_index。可选。
- -csv：用于将比对的数据结果写入csv文件中，配置该参数即开启，默认未配置，表示关闭，即将比对结果保存在txt文件中。
- [-custom：用户自定义Format转换.py文件存放路径，需指定到“format_convert”目录的上一层目录。可选。.py文件相关要求参见准备自定义Format转换.py文件](atlasaccuracy_16_0077.html#ZH-CN_TOPIC_0000002504343856__zh-cn_topic_0000002502563718_zh-cn_topic_0000001312632561_section6833162804213)。
不建议调用与当前用户不一致的其它用户目录下的自定义脚本文件，避免提权风险。

- -ffts：dump数据开启FFTS+模式，取值为：True：开启；False：关闭，默认关闭。可选。当前无场景支持此参数。

[请根据比对数据说明](atlasaccuracy_16_0073.html#ZH-CN_TOPIC_0000002504343854)中准备的数据类型，选择-f或-q参数项。

#### 比对步骤

Tensor比对命令行方式操作步骤：

- 本节涉及的.json文件、目录等名称均为举例，请根据实际环境替换；其中result和log日志路径需提前创建，并确保运行用户具有读写权限。
- 本节以非量化昇腾AI处理器运行生成的dump数据与非量化Caffe模型npy文件比对为例进行介绍，下文中参数说明均以该示例介绍，请根据您的比对数据选择不同场景加以替换理解。
- 不支持两份基于相同模型、昇腾AI处理器运行生成的dump数据进行单算子精度比对。

1. 登录开发环境。
2. 执行export命令设置环境变量并生成json文件。

设置环境变量：

```
export LD_LIBRARY_PATH=/home/xxx/Ascend/cann/lib64:${LD_LIBRARY_PATH}
```

生成json文件：
************
```
atc --mode=1 --om=$HOME/data/resnet50.om --json=$HOME/data/resnet50.json
atc --mode=5 --om=ge_proto_00005_Build.txt --json=ge_proto_00005_Build.txt.json
```

3. 进入${INSTALL_DIR}/tools/operator_cmp/compare，${INSTALL_DIR}请替换为CANN软件安装后文件存储路径。以root用户安装为例，则安装后文件存储路径为：/usr/local/Ascend/cann。
4. 执行Tensor比对命令，样例命令如下：
************************
```
python3 compare_vector.py -l $HOME/MyApp_mind/resnet50 -r $HOME/Standard_caffe/resnet50 -f $HOME/data/resnet50.json -o $HOME/result  -d pool5 -i 0
python3 compare_vector.py -l $HOME/MyApp_mind/resnet50 -r $HOME/Standard_tf/resnet50 -f $HOME/data/ge_proto_00005_Build.txt.json -o $HOME/result  -d gradients/AddN_63 -i 0
```

5. Tensor比对结果文件内容如图1和图2所示。
**图1**
单算子比对概要结果
单算子比对概要结果存放在“{op_name}_input_{index}_summary.txt”或“{op_name}_output_{index}_summary.txt”文件中，各参数说明如下：

  - TotalCount：该算子的dump数据的data个数。
  - LeftOp：表示My Output模型算子名。
  - RightOp：表示Ground Truth模型的算子名。
  - Format：数据格式。
  - MinAbsoluteError & MaxAbsoluteError：绝对误差的最小和最大值范围。
  - MinRelativeError & MaxRelativeError：相对误差的最小和最大值范围。
**图2**
单算子完整比对结果

单算子比对完整结果存放在“{op_name}_input_{index}_{file_index}.csv”或“{op_name}_output_{index}_{file_index}.csv”文件中，每个文件最多记录100万条数据。图2中各列参数说明如下：

  - N C H W：数据的坐标点。
  - Left：该列为My Output模型的算子dump值。
  - Right：该列为Ground Truth模型的算子dump值。
  - RelativeError：相对误差，AbsoluteError值除以Ground Truth模型算子的dump值比对出来的结果。当Ground Truth算子的dump值为0时，该处显示为“-”。
  - AbsoluteError：绝对误差，My Output模型算子的dump值减Ground Truth模型算子的dump值取绝对值比对出来的结果。

**父主题：**[Tensor比对](atlasaccuracy_16_0071.html)