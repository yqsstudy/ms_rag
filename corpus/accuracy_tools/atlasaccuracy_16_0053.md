---
title: "Top溢出算子解析"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/ModelAccuracyAnalyzer/atlasaccuracy_16_0053.html"
date_collected: "2026-05-04"
category: "accuracy_tools"
original_path: "zh/mindstudio/830/T&ITools/ModelAccuracyAnalyzer/atlasaccuracy_16_0053.html"
---

# Top溢出算子解析

[AI业务运行过程中可能存在算子溢出的情况，此时若直接进行精度比对操作则会造成比对结果不准确。通过执行查看溢出算子数据](atlasaccuracy_16_0052.html#ZH-CN_TOPIC_0000002504184006__zh-cn_topic_0000002502723530_section788711221975)，可以检测并收集溢出的算子信息，生成算子溢出数据文件和溢出算子的dump文件。

当生成的算子溢出数据文件和溢出算子的dump文件的落盘时间与算子溢出的时间不一致时，在这两个文件中则无法第一时间定位到第一个溢出的算子。

为了帮助用户快速定位溢出算子，本章节介绍的Top溢出算子解析，可以对生成的Debug file和溢出算子的dump文件进行分析，并展示TopN溢出算子的关键信息。

#### 命令格式说明

算子溢出检测命令行格式如下:

```
python3 msaccucmp.py overflow -d <dump_path> -out <output_path> [-n <topn>]
```

命令行参数说明如表1所示。

该功能通过msaccucmp.py脚本实现，脚本存放在${INSTALL_DIR}/tools/operator_cmp/compare，${INSTALL_DIR}请替换为CANN软件安装后文件存储路径。以root用户安装为例，则安装后文件存储路径为：/usr/local/Ascend/cann。
**表1**算子溢出检测命令行参数说明
**参数名**

**参数说明**

**是否必选**

-d

--dump_path

Debug file和溢出算子的dump文件所在目录。

[请参见查看溢出算子数据](atlasaccuracy_16_0052.html#ZH-CN_TOPIC_0000002504184006__zh-cn_topic_0000002502723530_section788711221975)获取文件目录。

目录下如果缺少dump文件，则会导致-out输出时缺少npy文件；如果目录下没有Debug file，则表示无溢出。

是

-out

--output_path

算子溢出分析结果文件输出目录。

输出文件包括：

- Debug file生成的json文件。过程文件，用于提取结果文件中topn溢出算子的算子名称和溢出信息。
- 溢出算子的dump数据生成的npy文件，包含算子的输入输出数据。过程文件，用于提取结果文件中算子溢出的关键信息。
- 算子溢出检测分析结果文件，汇总topn溢出算子的信息。结果文件，命名格式为“overflow_summary_{timestamp}.txt”。

缺少npy文件，会导致结果文件解析不到溢出算子的输入输出信息。

不建议配置与当前用户不一致的其它用户目录，避免提权风险。

是

-n

--topn

解析溢出的前N个算子，取值范围为1~5，默认值为1。

否
|  |  |  |
| --- | --- | --- |
|  |  |  |
|  |  |  |
|  |  |  |

#### 执行步骤

[使用以下步骤进行算子溢出分析之前请参见查看溢出算子数据](atlasaccuracy_16_0052.html#ZH-CN_TOPIC_0000002504184006__zh-cn_topic_0000002502723530_section788711221975)，对dump文件进行算子溢出检测，并生成Debug file和溢出算子的dump文件。

算子溢出检测命令行方式操作步骤：

-out指定的结果文件存放路径，请确保操作用户具有读写权限。

1. 登录CANN工具安装环境。
2. 进入${INSTALL_DIR}/tools/operator_cmp/compare，${INSTALL_DIR}请替换为CANN软件安装后文件存储路径。以root用户安装为例，则安装后文件存储路径为：/usr/local/Ascend/cann。
3. 执行算子溢出检测命令。
******
```
python3 msaccucmp.py overflow -d /MyApp20/dump -out /MyApp20/out -n 3
```

执行算子溢出检测结果overflow_summary_{timestamp}.txt文件内容如图1所示。
**图1**
溢出算子结果信息
结果文件信息中，根据展示数据从上到下顺序，展示信息如下：

  - 从1到n表示解析出第一个溢出的算子到第n个溢出的算子。
  - 每个溢出算子的类型和名称。
  - 算子的溢出信息，包括：溢出类型，溢出的任务ID，流ID和溢出错误码。
  - timestamp为算子溢出的时间戳。
  - *.input.*.npy为溢出算子的输入数据的npy文件。
  - *.input.*.npy文件名下方展示的是文件中算子溢出的输入关键信息，包括数据格式，数据维度，数据类型，最大值，最小值和均值。
  - *.output.*.npy为溢出算子的输出数据的npy文件。
  - *.output.*.npy文件名下方展示的是文件中算子溢出的输出关键信息，包括数据格式，数据维度，数据类型，最大值，最小值和均值。

**父主题：**[扩展功能](atlasaccuracy_16_0051.html)