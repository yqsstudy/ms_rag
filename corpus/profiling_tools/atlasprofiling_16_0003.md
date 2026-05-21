---
title: "离线推理场景性能分析快速入门"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0003.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0003.html"
---

# 离线推理场景性能分析快速入门

**离线推理场景下，推荐使用msprof命令行**方式采集和解析性能数据，并通过生成的结果文件分析性能瓶颈。

#### 前提条件

- 请确保安装CANN Toolkit开发套件包和ops算子包。
[参见《CANN 软件安装指南](https://www.hiascend.com/document/detail/zh/canncommercial/850/softwareinst/instg/instg_0000.html?Mode=PmIns&InstallType=local&OS=openEuler)》。

- 已完成应用程序功能调试，准备对应的可执行二进制文件或可执行脚本。

[下文根据昇腾AI处理器的PCIe工作模式区分为Ascend EP和Ascend RC两种操作步骤，Ascend EP和Ascend RC详细介绍请参见《昇腾产品形态说明](https://www.hiascend.com/document/detail/zh/AscendFAQ/ProduTech/productform/hardwaredesc_0001.html)》。

#### 采集、解析并导出性能数据（Ascend EP）

1. 登录装有CANN Toolkit开发套件包和ops算子包的运行环境，执行如下命令，可一键式采集、解析并导出性能数据：
************
```
msprof --output={path} {用户程序}
```

命令示例：
****************
```
msprof --output=/home/HwHiAiUser/profiling_output /home/HwHiAiUser/HIAI_PROJECTS/MyAppname/out/main
```
**表1**参数说明
参数

描述

**可选/必选**

--output

收集到的Profiling数据的存放路径，默认为AI任务文件所在目录。

路径中不能包含特殊字符："\n", "\\n", "\f", "\\f", "\r", "\\r", "\b", "\\b", "\t", "\\t", "\v", "\\v", "\u007F", "\\u007F", "\"", "\\\"", "'", "\'", "\\", "\\\\", "%", "\\%", ">", "\\>", "<", "\\<", "|", "\\|", "&", "\\&", "$", "\\$", ";", "\\;", "`", "\\`"。

可选

传入用户程序

<app> [app arguments]

请根据实际情况在msprof命令末尾添加AI任务执行命令来传入用户程序或执行脚本。

格式：msprof [msprof arguments] <app> [app arguments]

  - 举例1（msprof传入Python执行脚本和脚本参数）：msprof --output=/home/projects/output python3 /home/projects/MyApp/out/sample_run.py parameter1 parameter2
  - 举例2（msprof传入main二进制执行程序）：msprof --output=/home/projects/output main
  - 举例3（msprof传入main二进制执行程序）：msprof --output=/home/projects/output /home/projects/MyApp/out/main
  - 举例4（在msprof传入main二进制执行程序和程序参数）：msprof --output=/home/projects/output /home/projects/MyApp/out/main parameter1 parameter2
  - 举例5（msprof传入sh执行脚本和脚本参数）：msprof --output=/home/projects/output /home/projects/MyApp/out/sample_run.sh parameter1 parameter2

必选
|  |  |  |
| --- | --- | --- |
|  |  |  |
|  |  |  |

[以上为最基本的采集命令，如有其他采集需求，请参见性能数据采集和自动解析](atlasprofiling_16_0007.html#ZH-CN_TOPIC_0000002536038281)。

*命令执行完成后，在--output指定的目录下生成PROF_*XXX目录，存放自动解析后的性能数据（以下仅展示性能数据）。

```
 1
 2
 3
 4
 5
 6
 7
 8
 9
10
11
12
13
14
```

```
├── host   //保存原始数据，用户无需关注
...
│    └── data
├── device_{id}   //保存原始数据，用户无需关注
...
│    └── data
...
├── msprof_*.db
├── mindstudio_profiler_output
      ├── msprof_{timestamp}.json
      ├── step_trace_{timestamp}.json
      ├── xx_*.csv
       ...
      └── README.txt

```
|  |  |
| --- | --- |

2. 进入mindstudio_profiler_output目录，查看性能数据文件。

默认情况下采集到的文件如表2所示。
**表2**msprof默认配置采集的性能数据文件
文件名

说明

msprof_*.db

汇总所有性能数据的db格式文件。

仅Atlas A3 训练系列产品/Atlas A3 推理系列产品、Atlas A2 训练系列产品/Atlas A2 推理系列产品支持默认导出该文件。

msprof_*.json

timeline数据总表。

step_trace_*.json

迭代轨迹数据，每轮迭代的耗时。单算子场景下无此性能数据文件。

op_summary_*.csv

AI Core和AI CPU算子数据。

op_statistic_*.csv

AI Core和AI CPU算子调用次数及耗时统计。

step_trace_*.csv

迭代轨迹数据。单算子场景下无此性能数据文件。

task_time_*.csv

Task Scheduler任务调度信息。

fusion_op_*.csv

模型中算子融合前后信息。单算子场景下无此性能数据文件。

api_statistic_*.csv

用于统计CANN层的API执行耗时信息。

注：“*”表示时间戳。
|  |  |
| --- | --- |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |

  - [db文件推荐使用MindStudio Insight工具进行分析，详细介绍请参见《MindStudio Insight工具用户指南](https://www.hiascend.com/document/detail/zh/mindstudio/830/GUI_baseddevelopmenttool/msascendinsightug/Insight_userguide_0002.html)》。
  - **json文件需要在Chrome浏览器中输入chrome://tracing**，将文件拖到空白处进行打开，通过键盘上的快捷键（w：放大，s：缩小，a：左移，d：右移）。通过json文件可查看当前AI任务运行的时序信息，比如运行过程中接口调用时间线，如图1所示。**图1**
查看json文件
  - csv文件可直接打开查看。通过csv文件可以看到AI任务运行时的软硬件数据，比如各算子在AI处理器软硬件上的运行耗时，通过字段排序等可以快速找出需要的信息，如图2所示。**图2**
查看csv文件

#### 采集、解析并导出性能数据（Ascend RC）

1. 登录运行环境，进入msprof工具所在目录“/var”。
2. 执行如下命令采集性能数据。
************
```
./msprof --output={path} {用户程序}
```

命令示例：
****************
```
./msprof --output=/home/HwHiAiUser/profiling_output /home/HwHiAiUser/HIAI_PROJECTS/MyAppname/out/main
```
**表3**参数说明
参数

描述

**可选/必选**

--output

收集到的Profiling数据的存放路径，默认为AI任务文件所在目录。

路径中不能包含特殊字符："\n", "\\n", "\f", "\\f", "\r", "\\r", "\b", "\\b", "\t", "\\t", "\v", "\\v", "\u007F", "\\u007F", "\"", "\\\"", "'", "\'", "\\", "\\\\", "%", "\\%", ">", "\\>", "<", "\\<", "|", "\\|", "&", "\\&", "$", "\\$", ";", "\\;", "`", "\\`"。

可选

传入用户程序

<app> [app arguments]

请根据实际情况在msprof命令末尾添加AI任务执行命令来传入用户程序或执行脚本。

格式：msprof [msprof arguments] <app> [app arguments]

  - 举例1（msprof传入Python执行脚本和脚本参数）：msprof --output=/home/projects/output python3 /home/projects/MyApp/out/sample_run.py parameter1 parameter2
  - 举例2（msprof传入main二进制执行程序）：msprof --output=/home/projects/output main
  - 举例3（msprof传入main二进制执行程序）：msprof --output=/home/projects/output /home/projects/MyApp/out/main
  - 举例4（在msprof传入main二进制执行程序和程序参数）：msprof --output=/home/projects/output /home/projects/MyApp/out/main parameter1 parameter2
  - 举例5（msprof传入sh执行脚本和脚本参数）：msprof --output=/home/projects/output /home/projects/MyApp/out/sample_run.sh parameter1 parameter2

必选
|  |  |  |
| --- | --- | --- |
|  |  |  |
|  |  |  |

[以上为最基本的采集命令，如有其他采集需求，请参见性能数据采集和自动解析](atlasprofiling_16_0007.html#ZH-CN_TOPIC_0000002536038281)。

*命令执行完成后，在--output指定的目录下生成PROF_*XXX目录，目录结构如下。

```
1
2
3
4
5
6
```

```
├── device_{id}
│    ├── data
│    └── ...
└── host
│    ├── data
│    └── ...

```
|  |  |
| --- | --- |

3. *将PROF_*XXX目录上传到安装CANN Toolkit开发套件包和ops算子包的开发环境，执行以下命令进行数据解析。
****************
```
msprof --export=on --output=<dir>
```

参数

描述

**可选/必选**

--export

解析并导出性能数据。可选on或off，默认值为off。

若需导出个别模型（Model ID）/迭代（Iteration ID）的数据，可在msprof采集命令执行完成后重新执行msprof --export命令配置--model-id、--iteration-id参数。

*对于未解析的PROF_*XXX文件，自动解析后再导出。

示例：msprof --export=on --output=/home/HwHiAiUser

必选

--output

*性能数据文件目录。须指定为PROF_**XXX目录或PROF_*XXX目录的父目录，例如：/home/HwHiAiUser/profiler_data/PROF_XXX。

路径中不能包含特殊字符："\n", "\\n", "\f", "\\f", "\r", "\\r", "\b", "\\b", "\t", "\\t", "\v", "\\v", "\u007F", "\\u007F", "\"", "\\\"", "'", "\'", "\\", "\\\\", "%", "\\%", ">", "\\>", "<", "\\<", "|", "\\|", "&", "\\&", "$", "\\$", ";", "\\;", "`", "\\`"。

必选
|  |  |  |
| --- | --- | --- |
|  |  |  |
|  |  |  |

[更多解析命令介绍请参见离线解析](atlasprofiling_16_0015.html#ZH-CN_TOPIC_0000002536038287)。
*PROF_*XXX目录下会新增数据文件，目录结构如下：
```
1
2
3
4
5
6
7
8
9
```

```
├── device_{id}
│    ├── data
├── host
│    ├── data
│    └── ...
└── mindstudio_profiler_output
      ├── xx_*.csv
      ├── xx_*.json
...

```
|  |  |
| --- | --- |

1. 进入mindstudio_profiler_output目录，查看性能数据文件。

默认情况下采集到的文件如表4所示。
**表4**msprof默认配置采集的性能数据文件
文件名

说明

msprof_*.json

timeline数据总表。

step_trace_*.json

迭代轨迹数据，每轮迭代的耗时。单算子场景下无此性能数据文件。

op_summary_*.csv

AI Core和AI CPU算子数据。

op_statistic_*.csv

AI Core和AI CPU算子调用次数及耗时统计。

step_trace_*.csv

迭代轨迹数据。单算子场景下无此性能数据文件。

task_time_*.csv

Task Scheduler任务调度信息。

fusion_op_*.csv

模型中算子融合前后信息。单算子场景下无此性能数据文件。

api_statistic_*.csv

用于统计CANN层的API执行耗时信息。

注：“*”表示时间戳。
|  |  |
| --- | --- |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |

  - **json文件需要在Chrome浏览器中输入chrome://tracing**，将文件拖到空白处进行打开，通过键盘上的快捷键（w：放大，s：缩小，a：左移，d：右移）。通过json文件可查看当前AI任务运行的时序信息，比如运行过程中接口调用时间线，如图3所示。**图3**
查看json文件
  - csv文件可直接打开查看。通过csv文件可以看到AI任务运行时的软硬件数据，比如各算子在AI处理器软硬件上的运行耗时，通过字段排序等可以快速找出需要的信息，如图4所示。**图4**
查看csv文件

#### 性能分析

从上文我们可以看到，性能数据文件较多，分析方法也较灵活，以下介绍几个重要文件及分析方法。

- **通过msprof_*.json文件从整体角度查看AI任务运行的时序信息，进而分析出可能存在的瓶颈点。图5**
msprof_*.json文件示例
  - 区域1：CANN层数据，主要包含Runtime等组件以及Node（算子）的耗时数据。
  - 区域2：底层NPU数据，主要包含Ascend Hardware下各个Stream任务流的耗时数据和迭代轨迹数据、昇腾AI处理器系统数据等。
  - 区域3：展示timeline中各算子、接口的详细信息（单击各个timeline色块展示）。

从上图可以大致分析出耗时较长的API、算子、任务流等，并且根据对应的箭头指向找出对应的下发关系，分析执行推理过程中下层具体耗时较长的任务，查看区域3的耗时较长的接口和算子，再结合csv文件进行量化分析，定位出具体的性能瓶颈。

- **通过op_statistic_*.csv文件分析各类算子的调用总时间、总次数等，排查某类算子总耗时是否较长，进而分析这类算子是否有优化空间。图6**
op_statistic_*.csv文件示例
可以按照Total Time排序，找出哪类算子耗时较长。

- **通过op_summary_*.csv文件分析具体某个算子的信息和耗时情况，从而找出高耗时算子，进而分析该算子是否有优化空间。图7**
op_summary_*.csv文件示例
Task Duration字段为算子耗时信息，可以按照Task Duration排序，找出高耗时算子；也可以按照Task Type排序，查看不同核（AI Core和AI CPU）上运行的高耗时算子。