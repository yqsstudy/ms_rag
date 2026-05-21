---
title: "数据目录说明"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0204.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0204.html"
---

# 数据目录说明

性能数据落盘目录结构为：

- 调用tensorboard_trace_handler函数时的落盘目录结构：
  - MindSpore和PyTorch框架在该场景下输出的性能数据文件基本一致，以下将两种框架数据合并介绍，个别不同会在注释中说明。
  - [以下数据文件用户无需打开查看，可使用《MindStudio Insight工具用户指南](https://www.hiascend.com/document/detail/zh/mindstudio/830/GUI_baseddevelopmenttool/msascendinsightug/Insight_userguide_0002.html)》工具进行性能数据的查看和分析。

  - 若kernel_details.csv中出现StepID空值，用户可通过trace_view.json文件查看该算子的Step信息，或重新采集Profiling数据。
  - 以下数据是基于实际环境采集，若环境中无对应条件，则不会生成对应数据或文件，如模型无AICPU算子，那么即使执行采集也不会生成对应data_preprocess.csv文件。

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
25
26
27
28
29
30
31
32
33
34
35
36
37
38
```

```
└── localhost.localdomain_139247_20230628101435_ascend_pt    // 性能数据结果目录，命名格式：{worker_name}_{timestamp}_ascend_{framework}，默认情况下{worker_name}为{hostname}_{pid}，{timestamp}为时间戳，{framework}是MindSpore和PyTorch两个框架的简写（ms和pt）
    ├── profiler_info_{Rank_ID}.json    // 用于记录Profiler相关的元数据，PyTorch单卡场景时文件名不显示{Rank_ID}
    ├── profiler_metadata.json    // 用来保存用户通过add_metadata接口添加的信息和其他Profiler相关的元数据
    ├── ASCEND_PROFILER_OUTPUT    // MindSpore Profiler或Ascend PyTorch Profiler接口采集并解析的性能数据目录
    │   ├── analysis.db    // PyTorch多卡或集群等存在通信的场景下默认生成
    │   ├── api_statistic.csv    // profiler_level配置为Level0（仅MindSpore）、Level1或Level2级别时生成
    │   ├── ascend_mindspore_profiler_{Rank_ID}.db    // MindSpore场景export_type配置为Db类型时生成
    │   ├── ascend_pytorch_profiler_{Rank_ID}.db    // PyTorch场景默认生成，单卡场景时文件名不显示{Rank_ID}
    │   ├── communication_analyzer.db    // MindSpore多卡或集群等存在通信的场景下，export_type配置为Db类型时生成
    │   ├── communication.json    // 多卡或集群等存在通信的场景，为性能分析提供可视化数据基础，profiler_level配置为Level1或Level2级别时生成
    │   ├── communication_matrix.json    // 多卡或集群等存在通信的场景，为性能分析提供可视化数据基础，通信小算子基本信息文件，profiler_level配置为Level1或Level2级别时生成
    │   ├── dataset.csv    // MindSpore场景activities配置为CPU类型时生成
    │   ├── data_preprocess.csv    // profiler_level配置为Level2时生成
    │   ├── hccs.csv    // sys_interconnection配置True开启时生成
    │   ├── kernel_details.csv    // activities配置为NPU类型时生成
    │   ├── l2_cache.csv    // l2_cache配置True开启时生成
    │   ├── memory_record.csv    // profile_memory配置True开启时生成
    │   ├── minddata_pipeline_raw_{Rank_ID}.csv       // MindSpore场景data_process=配置True开启且调用mindspore.dataset模块时生成
    │   ├── minddata_pipeline_summary_{Rank_ID}.csv   // MindSpore场景data_process=配置True开启且调用mindspore.dataset模块时生成
    │   ├── minddata_pipeline_summary_{Rank_ID}.json  // MindSpore场景data_process=配置True开启且调用mindspore.dataset模块时生成
    │   ├── nic.csv    // sys_io配置True开启时生成
    │   ├── npu_module_mem.csv    // profile_memory配置True开启时生成
    │   ├── operator_details.csv    // MindSpore场景配置activities为CPU类型且record_shapes配置True开启时生成；PyTorch场景默认自动生成
    │   ├── operator_memory.csv    // profile_memory配置True开启时生成
    │   ├── op_statistic.csv    // AI Core和AI CPU算子调用次数及耗时数据
    │   ├── pcie.csv    // sys_interconnection配置True开启时生成
    │   ├── roce.csv    // sys_io配置True开启时生成
    │   ├── step_trace_time.csv    // 迭代中计算和通信的时间统计
    │   └── trace_view.json    // 记录整个AI任务的时间信息
    ├── FRAMEWORK    // 框架侧的原始性能数据，无需关注
    ├── logs    // 解析过程日志
    └── PROF_000001_20230628101435646_FKFLNPEPPRRCFCBA    // CANN层的性能数据，命名格式：PROF_{数字}_{时间戳}_{字符串}，data_simplification配置True开启时，仅保留此目录下的原始性能数据，删除其他数据
          ├── analyze    // 多卡或集群等存在通信的场景下，profiler_level配置为Level1或Level2级别时生成
          ├── device_{Rank_ID}    //  CANN Profiling采集的device侧的原始性能数据
          ├── host    // CANN Profiling采集的host侧的原始性能数据
          ├── mindstudio_profiler_log    // CANN Profiling解析的日志文件
          └── mindstudio_profiler_output    // CANN Profiling解析的性能数据
├── localhost.localdomain_139247_20230628101435_ascend_pt_op_arg    // PyTorch场景算子信息统计文件目录，record_op_args配置True开启时生成

```
|  |  |
| --- | --- |

[MindSpore Profiler和Ascend PyTorch Profiler接口将框架侧的数据与CANN Profiling的数据关联整合，形成trace、Kernel以及memory等性能数据文件。保存在ASCEND_PROFILER_OUTPUT目录下，包括json和csv格式的timeline和summary数据](atlasprofiling_16_0205.html#ZH-CN_TOPIC_0000002504198614)[、ascend_pytorch_profiler_{Rank_ID}.db数据](atlasprofiling_16_0206.html#ZH-CN_TOPIC_0000002504358450)[、analysis.db数据](atlasprofiling_16_0207.html#ZH-CN_TOPIC_0000002536038403)。

[PROF目录下为CANN Profiling采集的性能数据，主要保存在mindstudio_profiler_output目录下和msprof_*.db文件内，数据介绍请参见性能数据文件参考](atlasprofiling_16_0140.html#ZH-CN_TOPIC_0000002536158391)。

- PyTorch的场景调用export_chrome_trace方法时，Ascend PyTorch Profiler接口会将解析的trace数据写入到*.json文件中，其中*为文件名，不存在该文件时在指定路径下自动创建。
**父主题：**[MindSpore&PyTorch框架性能数据文件参考](atlasprofiling_16_0203.html)