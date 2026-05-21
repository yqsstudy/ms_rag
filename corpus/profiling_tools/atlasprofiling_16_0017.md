---
title: "查询性能数据文件信息"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0017.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0017.html"
---

# 查询性能数据文件信息

本功能用于查询性能数据文件信息，确认导出时指定迭代（Iteration ID）/模型（Model ID）。

性能数据解析时自动打印展示性能数据文件信息，故本功能在数据解析中为可选操作，主要用于已解析的历史PROF_XXX目录重新查询性能数据文件信息。

以下产品不支持在设备上直接查询，需要将采集到的PROF_XXX目录拷贝到安装了CANN Toolkit开发套件包和ops算子包的环境下进行查询：

- Atlas 200I/500 A2 推理产品的Ascend RC场景

#### 前提条件

[请确保完成使用前准备](atlasprofiling_16_0002.html#ZH-CN_TOPIC_0000002504358330)。

完成性能数据采集。

#### 操作步骤

执行查询命令。

命令示例如下：
****************
```
msprof --query=on --output=<dir>
```
**表1**参数说明
参数

说明

**可选/必选**

--query

查询性能数据文件信息。可选on或off，默认值为off。

当完成解析后，可以通过本参数查询性能数据文件信息。

必选

--output

*解析后的性能数据文件目录。须指定为PROF_XXX目录或PROF_*XXX目录的父目录，例如：/home/HwHiAiUser/profiler_data/PROF_XXX。

路径中不能包含特殊字符："\n", "\\n", "\f", "\\f", "\r", "\\r", "\b", "\\b", "\t", "\\t", "\v", "\\v", "\u007F", "\\u007F", "\"", "\\\"", "'", "\'", "\\", "\\\\", "%", "\\%", ">", "\\>", "<", "\\<", "|", "\\|", "&", "\\&", "$", "\\$", ";", "\\;", "`", "\\`"。

必选
|  |  |  |
| --- | --- | --- |
|  |  |  |
|  |  |  |

msprof工具的查询功能获取到的信息如表2所示。
**表2**Profiling数据文件信息
字段

含义

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

集群场景的节点识别ID。
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
**父主题：**[离线解析](atlasprofiling_16_0015.html)