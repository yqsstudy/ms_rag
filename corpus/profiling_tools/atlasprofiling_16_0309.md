---
title: "查询性能数据文件信息"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0309.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0309.html"
---

# 查询性能数据文件信息

本功能用于查询性能数据文件信息，确认导出时指定迭代（Iteration ID）/模型（Model ID）。

**执行查询操作前需要调用import**命令解析Profiling数据，否则查询结果无意义。

请参见如下步骤查询性能数据信息。

1. 以CANN-Toolkit开发套件包和ops算子包的运行用户登录开发环境。
2. 切换至msprof.py脚本所在目录。

${INSTALL_DIR}/tools/profiler/profiler_tool/analysis/msprof，${INSTALL_DIR}请替换为CANN软件安装后文件存储路径。若安装的Ascend-cann-toolkit软件包，以root安装举例，则安装后文件存储路径为：/usr/local/Ascend/ascend-toolkit/latest。

3. 查询性能数据信息，命令行格式如下。参数说明参见表1。
**********
```
python3 msprof.py query -dir <dir> 
```

**例如：python3 msprof.py query -dir**/home/HwHiAiUser/profiler_data/PROF_XXX
**表1**查询性能数据信息命令参数说明
参数名

**描述**

**可选/必选**

-dir或--collection-dir

*收集到的性能数据目录。须指定为PROF_XXX目录或PROF_*XXX目录的父目录，例如：

/home/HwHiAiUser/profiler_data/PROF_XXX

必选

--data-type

数据类型。用于MindStudio对接，用户无需配置。取值为：

  - 0：集群场景，可查询当前数据是否为集群场景采集的数据。
  - 1：迭代轨迹数据，每轮迭代的详细数据，包括FP/BP计算时间、迭代更新拖尾和迭代间隙。
  - 2：计算量，AI Core上的浮点运算数。
  - 3：数据准备，训练数据发送至Device以及Device侧读取训练数据。
  - 4：并行度调优建议。
  - 5：并行度数据，主要展示纯通信耗时和计算耗时。
  - 6：通信慢卡慢链路数据及优化建议。
  - 7：通信矩阵数据及优化建议。
  - 8：Host侧系统及进程的CPU、内存的性能指标。
  - 9：通信耗时使能关键路径分析。
  - 10：通信矩阵使能关键路径分析。

可选

--id

集群场景时指定集群节点的Rank ID，非集群场景指定设备ID。

用于MindStudio对接，用户无需配置。

可选

--model-id

模型ID。

用于MindStudio对接，用户无需配置。

可选

--iteration-id

指定以Graph为粒度统计的迭代ID（每个Graph执行一次，Iteration ID加1，当一个脚本被编译为多个Graph时，该ID与脚本层面的Step ID不一致）。默认值为1。

用于MindStudio对接，用户无需配置。

可选

-h或--help

显示帮助信息，仅在获取使用方式时使用。

可选
|  |  |  |
| --- | --- | --- |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |

执行上述命令后会打印显示结果。

msprof工具的查询功能获取到的信息如表2所示。
**表2**性能数据文件信息
字段

说明

Job Info

任务名。

Device ID

设备ID。

Dir Name

文件夹名称。

Collection Time

数据采集时间。

Model ID

模型ID。

Iteration Number

总迭代数。

Top Time Iteration

耗时最长的5个迭代。

Rank ID

集群场景的节点标识ID。
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

**父主题：**[使用msprof.py脚本解析与导出性能数据](atlasprofiling_16_0306.html)