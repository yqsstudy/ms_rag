---
title: "通过命令行方式分析比对结果"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/ModelAccuracyAnalyzer/atlasaccuracy_16_0042.html"
date_collected: "2026-05-04"
category: "accuracy_tools"
original_path: "zh/mindstudio/830/T&ITools/ModelAccuracyAnalyzer/atlasaccuracy_16_0042.html"
---

# 通过命令行方式分析比对结果

#### 命令格式说明

通过命令行方式分析比对结果是基于精度比对的基础上执行-advisor参数功能，完成精度比对之后继续进行专家系统分析并输出结果。

命令行格式如下：
****
```
python3 msaccucmp.py compare -m my_dump_path -g golden_dump_path -advisor
```
**表1**参数说明
**参数名**

**参数说明**

-advisor

在Tensor比对结束后，针对比对结果进行数据分析，给出专家建议。

**注：-overflow_detection参数为Float16溢出检测**专家建议提供数据，配置-advisor后会自动打开该参数功能。
|  |  |
| --- | --- |
|  |  |
|  |  |

#### 操作步骤

1. 登录CANN工具安装环境。
2. 生成json文件。
******
```
atc --mode=1 --om=$HOME/data/resnet50.om --json=$HOME/data/resnet50.json
```

3. 进入${INSTALL_DIR}/tools/operator_cmp/compare，${INSTALL_DIR}请替换为CANN软件安装后文件存储路径。以root用户安装为例，则安装后文件存储路径为：/usr/local/Ascend/cann。
4. 执行比对命令。
********
```
python3 msaccucmp.py compare -m $HOME/MyApp_mind/resnet50 -g $HOME/Standard_caffe/resnet50 -f $HOME/data/resnet50.json -out $HOME/result -advisor
```

5. [执行命令后会进行精度比对，比对完成后，系统将自动进行专家系统分析，并打印输出结果，结果文件命名为advisor_summary.txt，保存路径同样由-out参数确定。输出结果详细介绍请参见输出结果和优化建议](atlasaccuracy_16_0044.html#ZH-CN_TOPIC_0000002504184002)。
**父主题：**[比对结果专家建议](atlasaccuracy_16_0039.html)