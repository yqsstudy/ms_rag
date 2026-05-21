---
title: "通信性能数据解析"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0019.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0019.html"
---

# 通信性能数据解析

msprof通信性能数据解析功能主要用于统计通信类的分段耗时、拷贝信息、带宽等信息，以便进行通信类数据分析。通信类数据只有在多卡、多节点或集群场景下存在。

#### 前提条件

- [完成使用前准备](atlasprofiling_16_0002.html#ZH-CN_TOPIC_0000002504358330)。
- 对PROF_XXX目录已执行msprof的export（关闭clear）操作。

#### 操作步骤（msprof命令行方式）

执行分析命令。

命令示例如下：
******************************
```
msprof --analyze=on [--type=<type>] [--rule=communication] --output=<dir> [--clear=on]
```
**表1**参数说明
参数

说明

**可选/必选**

--analyze

分析性能数据文件，可选on或off，默认值为off。

必选

--type

设置性能数据解析结果文件格式，即可以选择msprof命令行执行后自动解析的结果文件格式，取值为：

- text：表示解析为json格式文件和communication_analyzer.db文件。
- db：表示解析为communication_analyzer.db文件。

默认为text。

可选

--rule

分析规则，取值为：

- communication：分析通信类数据。
  - --type=text时，在PROF_XXX/analyze目录下生成communication.json文件，展示单卡所有通信算子通信耗时、带宽等详细信息，如图4所示；以及生成communication_analyzer.db文件。
  - --type=db时，在PROF_XXX/analyze目录下仅生成communication_analyzer.db文件，保存CommAnalyzerTime（通信耗时）和CommAnalyzerBandwidth（通信带宽）信息表。

- communication_matrix：分析通信矩阵数据。
  - --type=text时，在PROF_XXX/analyze目录下生成communication_matrix.json文件，展示通信小算子基本的信息，包含通信size、通信带宽、通信rank等信息，用于分析通信细节，如图5所示；以及生成communication_analyzer.db文件。
  - --type=db时，在PROF_XXX/analyze目录下仅生成communication_analyzer.db文件，保存CommAnalyzerMatrix（通信矩阵）信息表。

**以上两个参数值可以同时配置，使用逗号分隔，例如：--rule**=communication,communication_matrix。

默认同时设置以上两个参数值。

可选

--output

*性能数据文件目录。须指定为PROF_*XXX目录，例如：/home/HwHiAiUser/profiler_data/PROF_XXX。

路径中不能包含特殊字符："\n", "\\n", "\f", "\\f", "\r", "\\r", "\b", "\\b", "\t", "\\t", "\v", "\\v", "\u007F", "\\u007F", "\"", "\\\"", "'", "\'", "\\", "\\\\", "%", "\\%", ">", "\\>", "<", "\\<", "|", "\\|", "&", "\\&", "$", "\\$", ";", "\\;", "`", "\\`"。

必选

--clear

数据精简模式，开启后将在导出性能数据后删除PROF_XXX目录下的sqlite目录，以节省存储空间。可选on或off，默认值为off。

可选
|  |  |  |
| --- | --- | --- |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |

#### 操作步骤（msprof.py脚本方式）

1. 以CANN Toolkit开发套件包和ops算子包的运行用户登录开发环境。
2. 切换至msprof.py脚本所在目录。

${INSTALL_DIR}/tools/profiler/profiler_tool/analysis/msprof，${INSTALL_DIR}请替换为CANN软件安装后文件存储路径。若安装的Ascend-cann-toolkit软件包，以root安装举例，则安装后文件存储路径为：/usr/local/Ascend/ascend-toolkit/latest。

3. 执行分析命令。
命令示例如下：****************************
```
python3 msprof.py analyze [--type <type>] --rule communication -dir <dir> [--clear]
```

**表2**参数说明
参数

说明

**可选/必选**

analyze

分析性能数据文件。

必选

--type

设置性能数据解析结果文件格式，即可以选择msprof.py脚本执行后自动解析的结果文件格式，取值为：

- text：表示解析为json格式文件和communication_analyzer.db文件。
- db：表示解析为communication_analyzer.db文件。

默认为text。

可选

-r或--rule

分析规则，取值为：

- communication：分析通信类数据。
  - --type text时，在PROF_XXX/analyze目录下生成communication.json文件，展示单卡所有通信算子通信耗时、带宽等详细信息，如图4所示；以及生成communication_analyzer.db文件。
  - --type db时，在PROF_XXX/analyze目录下仅生成communication_analyzer.db文件，保存CommAnalyzerTime（通信耗时）和CommAnalyzerBandwidth（通信带宽）信息表。

- communication_matrix：分析通信矩阵数据。
  - --type text时，在PROF_XXX/analyze目录下生成communication_matrix.json文件，展示通信小算子基本的信息，包含通信size、通信带宽、通信rank等信息，用于分析通信细节，如图5所示；以及生成communication_analyzer.db文件。
  - --type db时，在PROF_XXX/analyze目录下仅生成communication_analyzer.db文件，保存CommAnalyzerMatrix（通信矩阵）信息表。

**以上两个参数值可以二选一也可以同时配置，同时配置时使用逗号分隔，例如：--rule**communication,communication_matrix。

必选

-dir或--collection-dir

*性能数据文件目录。须指定为PROF_*XXX目录，例如：/home/HwHiAiUser/profiler_data/PROF_XXX。

路径中不能包含特殊字符："\n", "\\n", "\f", "\\f", "\r", "\\r", "\b", "\\b", "\t", "\\t", "\v", "\\v", "\u007F", "\\u007F", "\"", "\\\"", "'", "\'", "\\", "\\\\", "%", "\\%", ">", "\\>", "<", "\\<", "|", "\\|", "&", "\\&", "$", "\\$", ";", "\\;", "`", "\\`"。

必选

--clear

数据精简模式，开启后将在导出性能数据后删除PROF_XXX目录下的sqlite目录，以节省存储空间。配置该参数时表示开启数据精简模式，未配置表示关闭，默认关闭。

可选
|  |  |  |
| --- | --- | --- |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |

#### 解析结果

- **--type=text或--type=db以及--rule=communication图1**
CommAnalyzerTime**表3**CommAnalyzerTime
字段

说明

hccl_op_name

通信算子名称。

group_name

通信算子的分组。

start_timestamp

通信开始时间戳。

elapse_time

算子的通信总耗时，单位ms。

transit_time

通信时长，单位ms。表示通信算子的通信耗时，如果通信耗时过长，可能是某条链路存在问题。

wait_time

等待时长，单位ms。节点之间通信前首先需要进行同步，确保通信的两个节点同步完成，再进行通信。

synchronization_time

同步时长，单位ms。节点之间进行同步需要的时长。

idle_time

空闲时间，单位ms。空闲时间（idle_time） = 算子的通信总耗时（elapse_time） - 通信时长（transit_time） - 等待时长（wait_time）。
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
**图2**
CommAnalyzerBandwidth**表4**CommAnalyzerBandwidth
字段

说明

hccl_op_name

通信算子名称。

group_name

通信算子的分组。

transport_type

通信传输类型，包含：LOCAL、SDMA、RDMA、PCIE、HCCS、SIO。

transit_size

通信数据量，单位MB。

transit_time

通信时长，单位ms。表示通信算子的通信耗时，如果通信耗时过长，可能是某条链路存在问题。

bandwidth

通信带宽大小，单位GB/s。

large_packet_ratio

通信数据大包占比。

package_size

一次传输的通信数据包大小，单位MB。

count

通信传输次数。

total_duration

数据传输总耗时，单位ms。
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

- **--type=text或--type=db以及--rule=communication_matrix图3**
CommAnalyzerMatrix**表5**CommAnalyzerMatrix
字段

说明

hccl_op_name

通信算子名称。

group_name

通信算子的分组。

src_rank

通信源Rank。

dst_rank

通信目的Rank。

transport_type

通信传输类型，包含：LOCAL、SDMA、RDMA、PCIE、HCCS、SIO。

transit_size

通信数据量，单位MB。

transit_time

通信时长，单位ms。表示通信算子的通信耗时，如果通信耗时过长，可能是某条链路存在问题。

bandwidth

通信带宽大小，单位GB/s。
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

- --type=text、--rule=communication**图4**
communication.json
- --type=text、--rule=communication_matrix**图5**
communication_matrix.json
**父主题：**[离线解析](atlasprofiling_16_0015.html)