---
title: "比对操作和分析"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/ModelAccuracyAnalyzer/atlasaccuracy_16_0008.html"
date_collected: "2026-05-04"
category: "accuracy_tools"
original_path: "zh/mindstudio/830/T&ITools/ModelAccuracyAnalyzer/atlasaccuracy_16_0008.html"
---

# 比对操作和分析

#### 说明

- 本节中的计算图文件、目录等名称均为举例，请根据实际环境替换。其中，-out指定的结果存放路径，需确保操作用户具有读写权限。

- 如果执行过程中报“MemoryError”，则表示数据量过大导致了内存溢出，请将NPU的dump数据文件拆分到多个目录后，再逐一进行比对。
- 当指定的比对数据文件大小超过1GB或.json文件大小超过100MB时，比对过程可能耗时较长，系统提示：'The size (%d) of %s more than the XX, it needs more time to run.'。

#### 前提条件

[请确保完成使用前准备](atlasaccuracy_16_0002.html#ZH-CN_TOPIC_0000002504343822)。

#### 整网全算法维度比对并输出专家建议

将网络模型中参与计算的所有算子进行精度比对。操作步骤如下：

1. 登录CANN工具安装环境。
2. 生成json格式的计算图文件。
****
```
atc --mode=5 --om=ge_proto_00005_Build.txt --json=ge_proto_00005_Build.txt.json
```

[.txt格式计算图文件获取请参见准备NPU侧dump数据和计算图文件](atlasaccuracy_16_0007.html#ZH-CN_TOPIC_0000002504343824)。

3. 进入${INSTALL_DIR}/tools/operator_cmp/compare，${INSTALL_DIR}请替换为CANN软件安装后文件存储路径。以root用户安装为例，则安装后文件存储路径为：/usr/local/Ascend/cann。
4. 执行比对命令。
**整网全算法维度比对样例**：********
```
python3 msaccucmp.py compare -m $HOME/output/20200808163566/0/ge_default_20200808163719_121/11/0 -g $HOME/output/Standard_tf/resnet50 -f $HOME/data/ge_proto_00005_Build.txt.json -out $HOME/result -advisor
```

  - [上述命令仅展示当前场景所需参数的示例，若需要配置更多参数，比如已知可能出现精度问题的范围或因大型网络模型输出结果文件数据量过大，通过配置参数来减少输出结果的数据量，请参见命令格式说明](atlasaccuracy_16_0063.html#ZH-CN_TOPIC_0000002536143825)获取更多参数详细介绍。
  - 需要安装pandas 1.3或更高版本依赖，否则无法执行-advisor参数输出专家建议。
**表1**命令行参数说明
**参数名**

**参数说明**

是否必选

-m

--my_dump_path

基于昇腾AI处理器运行生成的训练/在线推理网络dump数据文件所在目录，须指定dump数据文件所在的父目录。

是

-g

--golden_dump_path

基于GPU运行生成的原始网络npy文件所在目录，须指定npy文件所在的父目录。

是

-f

--fusion_rule_file

全网层信息文件。

通过2使用ATC转换计算图文件生成的json文件。

是

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
比对结果如图1所示。**图1**
比对结果示例
[以上比对结果字段解释请参见完整比对结果参数说明](atlasaccuracy_16_0064.html#ZH-CN_TOPIC_0000002504184012)。

5. 比对结果分析。

[请参见比对结果分析](atlasaccuracy_16_0037.html#ZH-CN_TOPIC_0000002504343836)[。对于比对结果中可能存在部分无法比对或异常情况（例如结果中的NaN），请参见比对结果说明](atlasaccuracy_16_0036.html#ZH-CN_TOPIC_0000002504183998)。

**父主题：**[GPU vs NPU（TensorFlow 1.15训练/在线推理）](atlasaccuracy_16_0005.html)