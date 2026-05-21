---
title: "导出性能数据"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0310.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0310.html"
---

# 导出性能数据

[在导出性能数据前，需要参见解析性能数据](atlasprofiling_16_0308.html#ZH-CN_TOPIC_0000002536158481)解析性能数据。参见如下步骤导出性能数据。

1. 以CANN-Toolkit开发套件包和ops算子包的运行用户登录开发环境。
2. 切换至msprof.py脚本所在目录。

${INSTALL_DIR}/tools/profiler/profiler_tool/analysis/msprof，${INSTALL_DIR}请替换为CANN软件安装后文件存储路径。若安装的Ascend-cann-toolkit软件包，以root安装举例，则安装后文件存储路径为：/usr/local/Ascend/ascend-toolkit/latest。

3. 导出性能数据。可以导出timeline、summary和db三类文件，命令行格式如下：

  - 导出timeline数据和db文件**************************************
```
python3 msprof.py export timeline -dir <dir> [-reports <reports_sample_config.json>] [--iteration-id <iteration_id>] [--model-id <model-id>] [--iteration-count <iteration_count>] [--clear]
```

**例如：python3 msprof.py export timeline -dir**/home/HwHiAiUser/profiler_data/PROF_XXX

  - 导出summary数据和db文件**************************************
```
python3 msprof.py export summary -dir <dir> [--iteration-id <iteration_id>] [--model-id <model-id>] [--iteration-count <iteration_count>] [--format <export_format>] [--clear]
```

例如：python3 msprof.py export summary -dir /home/HwHiAiUser/profiler_data/PROF_XXX

  - 导出db文件**********
```
python3 msprof.py export db -dir <dir>
```

生成汇总所有性能数据的.db格式文件（msprof_时间戳.db）。

例如：python3 msprof.py export db -dir /home/HwHiAiUser/profiler_data/PROF_XXX

**表1**导出性能数据命令参数说明
参数名

**描述**

**可选/必选**

-dir或--collection-dir

*收集到的性能数据目录。须指定为PROF_XXX目录或PROF_*XXX目录的父目录，例如：

/home/HwHiAiUser/profiler_data/PROF_XXX

必选

-reports

[传入用户自定义的reports_sample_config.json配置文件，会根据配置文件中指定的范围导出相应的性能数据文件。参数实现与msprof --reports一致，详细介绍请参见--reports参数使用介绍](atlasprofiling_16_0018.html#ZH-CN_TOPIC_0000002504358344__zh-cn_topic_0000002502558624_section1128153151819)。

可选

--iteration-id

迭代ID。需配置为正整数。默认值为1。与--model-id必须同时配置。

  - 对于Atlas A2 训练系列产品/Atlas A2 推理系列产品，支持--model-id 4294967295，表示指定以Step为粒度统计的迭代ID（每执行完成一个Step，Iteration ID加1）。仅支持解析MindSpore（版本号大于等于2.3）框架的性能数据。
  - 对于Atlas A3 训练系列产品/Atlas A3 推理系列产品，支持--model-id 4294967295，表示指定以Step为粒度统计的迭代ID（每执行完成一个Step，Iteration ID加1）。仅支持解析MindSpore（版本号大于等于2.3）框架的性能数据。
  - --model-id配置为其他值时，指定以Graph为粒度统计的迭代ID（每个Graph执行一次，Iteration ID加1，当一个脚本被编译为多个Graph时，该ID与脚本层面的Step ID不一致）。

可选

--model-id

模型ID。需配置为正整数。与--iteration-id必须同时配置。

  - 对于Atlas A2 训练系列产品/Atlas A2 推理系列产品，支持--model-id 4294967295，为Step模式，即--iteration-id配置的值以Step为粒度解析。仅支持解析MindSpore（版本号大于等于2.3）框架的性能数据。
  - 对于Atlas A3 训练系列产品/Atlas A3 推理系列产品，支持--model-id 4294967295，为Step模式，即--iteration-id配置的值以Step为粒度解析。仅支持解析MindSpore（版本号大于等于2.3）框架的性能数据。
  - --model-id配置为其他值时，为Graph模式，即--iteration-id配置的值以Graph为粒度解析。

可选

--iteration-count

导出连续迭代的个数，取值范围为1~5的整数，根据--iteration-id配置的值为起始Step，导出连续数量的Step，比如配置--iteration-count为3，--iteration-id为1，则导出Step为1、2、3。

可选

--format

summary数据文件的导出格式，支持csv和json两种格式，默认值为csv。

仅配置summary参数时支持。

本文中summary文件介绍均以csv文件为例。

可选

--clear

数据精简模式，开启后将在导出性能数据后删除PROF_XXX/device_{id}下的sqlite目录，以节省存储空间。配置该参数时表示开启数据精简模式，未配置表示关闭，默认关闭。

可选

-h或--help

显示帮助信息，仅在获取使用方式时使用。

可选

注1：默认情况下，导出所有性能数据。

[注2：单算子场景和仅执行采集昇腾AI处理器系统数据](atlasprofiling_16_0010.html#ZH-CN_TOPIC_0000002504358338)场景，不支持--iteration-id和--model-id参数。
|  |  |  |
| --- | --- | --- |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |

4. 执行完上述命令后，会在collection-dir目录下的PROF_XXX目录下生成mindstudio_profiler_output目录和msprof_*.db文件。

**生成的Profiling数据**目录结构如下所示。

  - 单采集进程
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
└── PROF_XXX
      ├── device_0
      │    └── data
      ├── device_1
      │    └── data
      ├── host
      │    └── data
      ├── msprof_*.db
      └── mindstudio_profiler_output
            ├── msprof_{timestamp}.json
            ├── step_trace_{timestamp}.json
            ├── xx_*.csv
             ...
            └── README.txt

```
|  |  |
| --- | --- |

  - 多采集进程
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
15
16
17
18
19
20
21
22
23
24
```

```
└── PROF_XXX1
      ├── device_0
      │    └── data
      ├── host
      │    └── data
      ├── msprof_*.db
      └── mindstudio_profiler_output
            ├── msprof_{timestamp}.json
            ├── step_trace_{timestamp}.json
            ├── xx_*.csv
             ...
            └── README.txt
└── PROF_XXX2
      ├── device_1
      │    └── data
      ├── host
      │    └── data
      ├── msprof_*.db
      └── mindstudio_profiler_output
            ├── msprof_{timestamp}.json
            ├── step_trace_{timestamp}.json
            ├── xx_*.csv
             ...
            └── README.txt

```
|  |  |
| --- | --- |


  - 多Device场景下，若启动单采集进程，则仅生成一个PROF_XXX目录，若启动多采集进程则生成多个PROF_XXX目录，其中device目录在PROF_XXX目录下生成，每个PROF_XXX目录下生成多少个device目录与用户实际操作有关，不影响性能数据分析。
  - [性能数据详细介绍请参见性能数据文件参考](atlasprofiling_16_0140.html#ZH-CN_TOPIC_0000002536158391)。
  - mindstudio_profiler_output目录中的文件是根据采集的实际性能数据进行生成，如果实际的性能数据没有相关的数据文件，就不会导出对应的timeline和summary数据。
  - 使用export命令能直接从已解析的性能数据中导出数据文件。当性能数据未解析时，单独执行export命令也能进行解析性能数据并导出数据文件。
  - **对于被强制中断的msprof采集进程，工具会保存已采集的原始性能数据，也可以使用export**解析并导出。

**父主题：**[使用msprof.py脚本解析与导出性能数据](atlasprofiling_16_0306.html)