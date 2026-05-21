---
title: "通过脚本工具方式分析比对结果"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/ModelAccuracyAnalyzer/atlasaccuracy_16_0043.html"
date_collected: "2026-05-04"
category: "accuracy_tools"
original_path: "zh/mindstudio/830/T&ITools/ModelAccuracyAnalyzer/atlasaccuracy_16_0043.html"
---

# 通过脚本工具方式分析比对结果

#### 脚本工具介绍

专家系统提供“mscmp_advisor.py”脚本工具。功能及安装路径如下：
**表1**脚本工具介绍
脚本名

功能

路径

“mscmp_advisor.py”

对Tensor比对结果进行专家系统分析，并输出优化建议。

${INSTALL_DIR}/tools/operator_cmp/compare，${INSTALL_DIR}请替换为CANN软件安装后文件存储路径。以root用户安装为例，则安装后文件存储路径为：/usr/local/Ascend/cann。
|  |  |  |
| --- | --- | --- |
|  |  |  |

#### 命令格式说明

“mscmp_advisor.py”脚本是直接用比对结果.csv文件进行分析，所以在进行该操作前需要先完成精度比对获取.csv文件。

命令行格式如下：

```
python3 mscmp_advisor.py -i <input_file> [-input_nodes <node_name>] [-o <out_path>]
```

**表2**参数说明
**参数名**

**参数说明**

**是否必选**

-i

--input_file

指定比对结果.csv文件。例如：$HOME/result/result_*.csv

本参数最大支持.csv文件的大小为100M。

是

-input_nodes

指定网络模型的输入节点。多个节点用英文分号（;）隔开。例如："node_name1;node_name2;node_name3"

否

若不配置，则不进行输入检测。

-o

--out_path

分析结果输出路径。结果文件命名为advisor_summary.txt。

不建议配置与当前用户不一致的其它用户目录，避免提权风险。

否

若不配置，不落盘结果文件。
|  |  |  |
| --- | --- | --- |
|  |  |  |
|  |  |  |
|  |  |  |

#### 操作步骤

1. 登录CANN工具安装环境。
2. 生成json文件。
******
```
atc --mode=1 --om=$HOME/data/resnet50.om --json=$HOME/data/resnet50.json
```

3. 配置环境变量。

```
export PYTHONPATH=${INSTALL_DIR}/tools/operator_cmp/compare:$PYTHONPATH
```

4. 执行精度比对命令。
********
```
python3 msaccucmp.py compare -m $HOME/MyApp_mind/resnet50 -g $HOME/Standard_caffe/resnet50 -f $HOME/data/resnet50.json -out $HOME/result -overflow_detection
```

**此处需要配置-overflow_detection***参数识别溢出算子。执行比对后输出比对结果文件result_*.csv。*

5. 执行专家系统分析。
********
```
python3 mscmp_advisor.py -i $HOME/result/result_*.csv -input_nodes "node_name1;node_name2;node_name3" -o $HOME/result
```

6. [执行命令后进行专家系统分析并直接打印输出结果。输出结果详细介绍请参见输出结果和优化建议](atlasaccuracy_16_0044.html#ZH-CN_TOPIC_0000002504184002)。
**父主题：**[比对结果专家建议](atlasaccuracy_16_0039.html)