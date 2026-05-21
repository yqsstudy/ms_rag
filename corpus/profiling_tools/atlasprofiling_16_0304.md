---
title: "获取设备信息"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0304.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0304.html"
---

# 获取设备信息

#### 工具介绍

*性能数据采集完成后可以通过“get_msprof_info.py”脚本工具在PROF_XXX目录下的device_{**id**}*或host目录文件获取设备信息。“get_msprof_info.py”功能及安装路径如下。
**表1**脚本介绍
脚本名

功能

路径

“get_msprof_info.py”

获取设备信息。

${INSTALL_DIR}/tools/profiler/profiler_tool/analysis/interface，${INSTALL_DIR}请替换为CANN软件安装后文件存储路径。若安装的Ascend-cann-toolkit软件包，以root安装举例，则安装后文件存储路径为：/usr/local/Ascend/ascend-toolkit/latest。
|  |  |  |
| --- | --- | --- |
|  |  |  |

#### 操作步骤

1. 以运行用户登录CANN-Toolkit开发套件包和ops算子包所在环境。
2. 切换至“get_msprof_info.py”脚本所在目录。
3. 执行“get_msprof_info.py”脚本，命令示例如下。

  - 非集群场景
```
python3 get_msprof_info.py -dir /home/1/PROF_000001_20220129014731273_KEDKPORHMAGPGD/device_0
```

  - 集群场景
```
python3 get_msprof_info.py -dir /home/1/
```

**表2**参数说明
参数名

**描述**

**可选/必选**

-dir或--collection-dir

*收集到的Profiling数据目录。非集群场景须指定为PROF_XXX目录下的host或device_{**id**}**目录；集群场景须指定为PROF_*XXX目录的父目录。

必选

-h或--help

显示帮助信息，仅在获取使用方式时使用。

可选
|  |  |  |
| --- | --- | --- |
|  |  |  |
|  |  |  |

4. 查看输出结果。

非集群场景会打印输出结果，如图1所示，各字段含义如表3所示；集群场景在-dir参数指定目录下生成/query/cluster_info.json文件保存集群场景各节点信息，如图2所示，各字段含义如表4所示。
**图1**
设备信息（非集群场景）**表3**字段说明（非集群场景）
字段

**说明**

collection_info

信息收集。

Collection end time

信息收集结束时间。

Collection start time

信息收集开始时间。

Result Size

信息数据大小，单位MB。

device_info

设备信息。

AI Core Number

AI Core数量。

AI CPU Number

AI CPU数量。

Control CPU Number

Control CPU数量。

Control CPU Type

Control CPU类型。

Device Id

设备ID。

TS CPU Number

TS CPU数量。

host_info

Host信息。

cpu_info

Host CPU信息。

CPU ID

Host CPU ID。

Name

Host CPU名称。

Type

Host CPU类型。

Frequency

Host CPU频率。

Logical_CPU_Count

Host逻辑CPU数量。

cpu_num

Host CPU数量。

Host Computer Name

Host设备名。

Host Operating System

Host操作系统。

model_info

模型信息。

Device Id

设备ID。

iterations

迭代统计。

Iteration Number

迭代次数。

Model Id

模型ID，根据模型数量显示。

version_info

版本信息。

analysis_version

解析版本信息。

collection_version

采集版本信息。

drv_version

驱动版本信息。
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
**图2**
设备信息（集群场景）**表4**字段说明（集群场景）
字段

**说明**

Rank Id

集群场景的节点标识ID，集群场景下设备的唯一标识。

Device Id

设备ID，集群场景下不作为设备唯一标识。

Prof Dir

集群场景下当前Rank Id对应设备上的PROF_XXX目录。

Device Dir

*集群场景PROF_XXX目录下的device_{**id**}*目录。

Models

模型信息，包含当前Rank Id对应设备的所有模型ID（Model ID）及该模型下的迭代次数（Iterations）。
|  |  |
| --- | --- |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |

**父主题：**[附录](atlasprofiling_16_0209.html)