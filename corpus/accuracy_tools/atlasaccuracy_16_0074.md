---
title: "整网比对"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/ModelAccuracyAnalyzer/atlasaccuracy_16_0074.html"
date_collected: "2026-05-04"
category: "accuracy_tools"
original_path: "zh/mindstudio/830/T&ITools/ModelAccuracyAnalyzer/atlasaccuracy_16_0074.html"
---

# 整网比对

#### 命令格式说明

Tensor比对命令行格式如下:

```
python3 compare_vector.py -l <LEFT_DUMP_PATH> -r <RIGHT_DUMP_PATH> [-f <FUSION_JSON_FILE_PATH>] [-q <QUANT_FUSION_RULE_FILE_PATH>] -o <OUTPUT_PATH> [-custom <CUSTOM_PATH>]
python3 compare_vector.py -l <LEFT_DUMP_PATH> -r <RIGHT_DUMP_PATH> -f <FUSION_JSON_FILE_PATH> -o <OUTPUT_PATH> [-custom <CUSTOM_PATH>]
```

- -l：My Output模型的比对数据文件目录。
- -r：Ground Truth模型的比对数据文件目录。
- -o：比对数据结果存储目录及文件名。
不建议配置与当前用户不一致的其它用户目录，避免提权风险。

- -f：全网层信息文件（通过使用ATC转换.om模型文件生成的json文件或转换.txt图文件生成的json文件）。可选。
- -q：量化融合规则文件。可选。
- -csv：用于将比对的数据结果写入csv文件中，配置该参数即开启，默认未配置，表示关闭，即将比对结果保存为普通文本文件。可选
- [-custom：用户自定义Format转换.py文件存放路径，需指定到“format_convert”目录的上一层目录。可选。.py文件相关要求参见准备自定义Format转换.py文件](atlasaccuracy_16_0077.html#ZH-CN_TOPIC_0000002504343856__zh-cn_topic_0000002502563718_zh-cn_topic_0000001312632561_section6833162804213)。
不建议调用与当前用户不一致的其它用户目录下的自定义脚本文件，避免提权风险。

- -ffts：dump数据开启FFTS+模式，取值为：True：开启；False：关闭，默认关闭。可选。当前无场景支持此参数。

[请根据比对数据说明](atlasaccuracy_16_0073.html#ZH-CN_TOPIC_0000002504343854)中准备的数据类型，选择-f或-q参数项。

#### 比对步骤

Tensor比对命令行方式操作步骤：

- 本节涉及的.json文件、目录等名称均为举例，请根据实际环境替换；其中result和log日志路径需提前创建，并确保运行用户具有读写权限。
- 本节以非量化昇腾AI处理器运行生成的dump数据与非量化Caffe模型npy文件比对为例进行介绍，下文中参数说明均以该示例介绍，请根据您的比对数据选择不同场景加以替换理解。
- 如果是两份基于相同模型、昇腾AI处理器运行生成的dump数据进行精度比对，需确保input个数、output个数、Format、Shape必须完全一致，否则无法比对；另外，此场景下命令行只需要带-l、-r、-o参数，不需要输入-f、-q参数。

1. 登录开发环境。
2. 执行export命令设置环境变量并生成json文件。

  1. 设置环境变量
```
export LD_LIBRARY_PATH=/home/xxx/Ascend/cann/lib64:${LD_LIBRARY_PATH}
```

  2. 生成json文件************
```
atc --mode=1 --om=$HOME/data/resnet50.om --json=$HOME/data/resnet50.json
atc --mode=5 --om=ge_proto_00005_Build.txt --json=ge_proto_00005_Build.txt.json
```

3. 进入/home/xxx/Ascend/cann/tools/operator_cmp/compare目录。
4. 执行Tensor比对命令，样例命令如下：
****************
```
python3 compare_vector.py -l $HOME/MyApp_mind/resnet50 -r $HOME/Standard_caffe/resnet50 -f $HOME/data/resnet50.json -o $HOME/result/result.txt
python3 compare_vector.py -l $HOME/MyApp_mind/resnet50 -r $HOME/Standard_tf/resnet50 -f $HOME/data/ge_proto_00005_Build.txt.json -o $HOME/result/result.txt
```

**如果需要保存为csv格式文件，可以修改命令为：-o $HOME/result/result.csv -csv**

5. Tensor比对结果result.txt文件内容如图1和图2所示。
**图1**
比对结果（推理）**图2**
比对结果（训练）
参数解释如下：

  - LeftOp：表示My Output模型的算子名。
  - RightOp：表示Ground Truth模型的算子名。
  - TensorIndex：表示My Output模型算子的input ID和output ID。
  - CosineSimilarity：进行余弦相似度算法比对出来的结果，范围是[-1,1]，比对的结果如果越接近1，表示两者的值越相近，越接近-1意味着两者的值越相反。
  - MaxAbsoluteError：进行最大绝对误差算法比对出来的结果，值越接近于0，表明越相近，值越大，表明差距越大。
  - AccumulatedRelativeError：进行累积相对误差算法比对出来的结果，值越接近于0，表明越相近，值越大，表明差距越大。
  - RelativeEuclideanDistance：进行欧氏相对距离算法比对出来的结果，值越接近于0，表明越相近，值越大，表明差距越大。
  - KullbackLeiblerDivergence：进行KL散度算法比对出来的结果，取值范围是0到无穷大。KL散度越小，真实分布与近似分布之间的匹配越好。
  - StandardDeviation：进行标准差算法比对出来的结果，取值范围：0到无穷大。标准差越小，离散度越小，表明越接近平均值。该列显示My Output和Ground Truth两组数据的均值和标准差，第一组展示My Output模型dump数据的数值（均值和标准差），第二组展示Ground Truth模型dump数据的数值（均值和标准差）。
  - 显示“*”，表示在NPU侧新增的算子无对应的标准算子；“NaN”表示无比对结果。
  - 余弦相似度和KL散度比对结果为NaN，其他算法有比对数据，则表明左侧或右侧数据为0；KL散度比对结果为inf，表明右侧数据有一个为0；比对结果为nan，表示dump数据有nan。

**父主题：**[Tensor比对](atlasaccuracy_16_0071.html)