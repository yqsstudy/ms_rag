---
title: "使用msprof-analyze工具分析性能数据"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/msquickstart/atlasquick_train_0017.html"
date_collected: "2026-05-04"
category: "quickstart"
original_path: "zh/mindstudio/830/msquickstart/atlasquick_train_0017.html"
---

# 使用msprof-analyze工具分析性能数据

#### 前提条件

1. [完成环境准备](atlasquick_train_0002.html#ZH-CN_TOPIC_0000002502572164__section68892049173411)。
2. [完成性能数据采集](atlasquick_train_0015.html)，得到昇腾NPU环境的性能数据。
3. 安装msprof-analyze，命令如下：
```
pip install msprof-analyze
```

提示出现如下信息则表示安装成功。

```
1
```

```
Successfully installed msprof-analyze-{version}

```
|  |  |
| --- | --- |

[msprof-analyze工具详细介绍请参见《msprof-analyze](https://gitcode.com/Ascend/mstt/tree/br_release_MindStudio_8.3.0_20261231/profiler/msprof_analyze)》。

#### 执行msprof-analyze分析

以下仅提供操作指导，无具体数据分析。

msprof-analyze主要以基于通信域的迭代内耗时分析、通信时间分析以及通信矩阵分析为主，从而定位慢卡、慢节点以及慢链路问题。

操作如下：

1. 数据准备。
将所有Device下的性能数据拷贝到同一目录下。

2. 执行性能分析操作。**
```
msprof-analyze -m all -d $HOME/profiling_data/
```

分析结果在-d参数指定目录下生成cluster_analysis_output文件夹并输出cluster_step_trace_time.csv、cluster_communication_matrix.json、cluster_communication.json文件。

[更多介绍请参见《msprof-analyze](https://gitcode.com/Ascend/mstt/tree/br_release_MindStudio_8.3.0_20261231/profiler/msprof_analyze)》。

[集群分析工具的交付件通过MindStudio Insight工具展示，详细操作请参见使用MindStudio Insight工具可视化性能数据](atlasquick_train_0018.html)。

#### 执行advisor分析

msprof-analyze的advisor功能是将MindSpore Profiler采集并解析出的性能数据进行分析，并输出性能调优建议。

命令如下：
**
```
msprof-analyze advisor all -d $HOME/profiling_data/
```

分析结果输出相关简略建议到执行终端中，并在命令执行目录下生成“mstt_advisor_{timestamp}.html”和“/log/mstt_advisor_{timestamp}.xlsx”文件供用户查看。

advisor工具的分析结果主要提供可能存在性能问题的专家建议。

[详细结果介绍请参见《advisor](https://gitcode.com/Ascend/mstt/tree/br_release_MindStudio_8.3.0_20261231/profiler/msprof_analyze/advisor)[》中的“报告解析](https://gitcode.com/Ascend/mstt/tree/br_release_MindStudio_8.3.0_20261231/profiler/msprof_analyze/advisor#报告解析（无标杆）)”。

#### 执行compare_tools性能比对

compare_tools功能用于对比不同框架或其他软件版本下，采集同一训练工程昇腾NPU环境性能数据之间的差异。
命令如下：********
```
msprof-analyze compare -d $HOME/2.7.0/profiling_data/*_ascend_ms -bp $HOME/2.6.0/profiling_data/*_ascend_ms --output_path ./compare_result/profiler_compare
```

分析结果输出到执行终端中，并在--output_path参数指定路径下生成“performance_comparison_result_{timestamp}.xlsx”文件供用户查看。

[性能比对工具将总体性能拆解为训练耗时和内存占用，其中训练耗时可拆分为算子（包括nn.Module）、通信、调度三个维度，并打印输出总体指标，帮助用户定位劣化的方向。与此同时，工具还会在“performance_comparison_result_{timestamp}.xlsx”文件中展示每个算子在执行耗时、通信耗时、内存占用的优劣，可通过DIFF列大于0筛选出劣化算子。此处不提供示例，详细结果介绍请参见《性能比对工具](https://gitcode.com/Ascend/mstt/tree/master/profiler/msprof_analyze/compare_tools)[》中的“比对结果说明](https://gitcode.com/Ascend/mstt/tree/br_release_MindStudio_8.3.0_20261231/profiler/msprof_analyze/compare_tools#比对结果说明)”。
**父主题：**[性能数据分析](atlasquick_train_0016.html)