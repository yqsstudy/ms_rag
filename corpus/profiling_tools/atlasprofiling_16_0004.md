---
title: "PyTorch训练场景性能分析快速入门"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0004.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0004.html"
---

# PyTorch训练场景性能分析快速入门

**PyTorch训练场景下，推荐通过Ascend PyTorch Profiler**接口采集并解析性能数据，用户可以根据结果自行分析和识别性能瓶颈。

**Ascend PyTorch Profiler**接口进行采集任务时，进程与Device之间的关系如下：

- 多进程多Device场景：支持每个Device下分别设置一个采集进程。
- 单进程多Device场景：支持。须配套PyTorch 2.1.0post14、2.5.1post2、2.6.0及之后的版本。
- 多进程单Device场景：需要保证多进程之间的采集动作是串行的，即各个采集动作不在同一时间开始，且各个采集动作须包含完整的启动和停止。

#### 前提条件

- 请确保安装CANN Toolkit开发套件包和ops算子包。
[参见《CANN 软件安装指南](https://www.hiascend.com/document/detail/zh/canncommercial/850/softwareinst/instg/instg_0000.html?Mode=PmIns&InstallType=local&OS=openEuler)》。

- [准备好基于PyTorch 2.1.0或更高版本开发的训练模型以及配套的数据集，并按照《PyTorch 训练模型迁移调优指南](https://www.hiascend.com/document/detail/zh/Pytorch/730/ptmoddevg/trainingmigrguide/PT_LMTMOG_0002.html)[》中的“模型迁移](https://www.hiascend.com/document/detail/zh/Pytorch/730/ptmoddevg/trainingmigrguide/PT_LMTMOG_0013.html)”完成PyTorch原始模型向昇腾AI处理器的迁移。

#### 采集并解析性能数据

1. **使用Ascend PyTorch Profiler**接口开启PyTorch训练时的性能数据采集。

在训练脚本（如train_*.py文件）内添加如下示例代码进行性能数据采集参数配置，之后启动训练。

  - [下列示例中的接口详细介绍请参见Ascend PyTorch Profiler接口说明](atlasprofiling_16_0121.html#ZH-CN_TOPIC_0000002504198570__zh-cn_topic_0000002534478481_section5699454151510)。
  - [PyTorch场景性能数据采集详细介绍请参见Ascend PyTorch调优工具](atlasprofiling_16_0120.html#ZH-CN_TOPIC_0000002536158381)。
  - 性能数据会占据一定的磁盘空间，可能存在磁盘写满导致服务器不可用的风险。性能数据所需空间跟模型的参数、采集开关配置、采集的迭代数量有较大关系，须用户自行保证落盘目录下的可用磁盘空间。

  - 示例一：使用with语句调用torch_npu.profiler.profile接口，自动创建Profiler，采集with范围内代码段的性能数据。
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
```

```
import torch
import torch_npu

...

experimental_config = torch_npu.profiler._ExperimentalConfig(
    export_type=[
        torch_npu.profiler.ExportType.Text
        ],
    profiler_level=torch_npu.profiler.ProfilerLevel.Level0,
    mstx=False,    # 原参数名msprof_tx改为mstx，新版本依旧兼容原参数名msprof_tx
    aic_metrics=torch_npu.profiler.AiCMetrics.AiCoreNone,
    l2_cache=False,
    op_attr=False,
    data_simplification=False,
    record_op_args=False,
    gc_detect_threshold=None
)

with torch_npu.profiler.profile(
    activities=[
        torch_npu.profiler.ProfilerActivity.CPU,
        torch_npu.profiler.ProfilerActivity.NPU
        ],
    schedule=torch_npu.profiler.schedule(wait=0, warmup=0, active=1, repeat=1, skip_first=1),    # 与prof.step()配套使用
    on_trace_ready=torch_npu.profiler.tensorboard_trace_handler("./result"),
    record_shapes=False,
    profile_memory=False,
    with_stack=False,
    with_modules=False,
    with_flops=False,
    experimental_config=experimental_config) as prof:

    for step in range(steps):
        train_one_step(step, steps, train_loader, model, optimizer, criterion)
        prof.step()    # 与schedule配套使用

```
|  |  |
| --- | --- |

  - **示例二：创建torch_npu.profiler.profile对象，**通过start和stop接口控制采集性能数据，用户可自定义采集启动的位置。
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
```

```
import torch
import torch_npu
...

experimental_config = torch_npu.profiler._ExperimentalConfig(
    export_type=[
        torch_npu.profiler.ExportType.Text
        ],
    profiler_level=torch_npu.profiler.ProfilerLevel.Level0,
    mstx=False,    # 原参数名msprof_tx改为mstx，新版本依旧兼容原参数名msprof_tx
    aic_metrics=torch_npu.profiler.AiCMetrics.AiCoreNone,
    l2_cache=False,
    op_attr=False,
    data_simplification=False,
    record_op_args=False,
    gc_detect_threshold=None
)

prof = torch_npu.profiler.profile(
    activities=[
        torch_npu.profiler.ProfilerActivity.CPU,
        torch_npu.profiler.ProfilerActivity.NPU
        ],
    schedule=torch_npu.profiler.schedule(wait=0, warmup=0, active=1, repeat=1, skip_first=1),    # 与prof.step()配套使用
    on_trace_ready=torch_npu.profiler.tensorboard_trace_handler("./result"),
    record_shapes=False,
    profile_memory=False,
    with_stack=False,
    with_modules=False,
    with_flops=False,
    experimental_config=experimental_config)

prof.start()    # 启动性能数据采集
for step in range(steps):
    train_one_step()
    prof.step()    # 与schedule配套使用
prof.stop()    # 结束性能数据采集

```
|  |  |
| --- | --- |

以上两个示例主要使用tensorboard_trace_handler导出性能数据，也可以使用以下prof.export_chrome_trace方式导出单个性能文件“chrome_trace_{pid}.json”。由于tensorboard_trace_handler导出的性能数据包含了prof.export_chrome_trace导出的性能数据，所以根据实际需求选择一种方式即可。

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
```

```
import torch
import torch_npu

...

with torch_npu.profiler.profile() as prof:

    # 启动性能数据采集
    for step in range(steps):
        train_one_step(step, steps, train_loader, model, optimizer, criterion)
prof.export_chrome_trace('./chrome_trace_14.json')

```
|  |  |
| --- | --- |

2. 查看采集到的性能数据结果文件。

**训练结束后，在torch_npu.profiler.tensorboard_trace_handler**接口指定的目录下生成Ascend PyTorch Profiler接口的采集结果目录，如下示例。

[以下数据文件用户无需打开查看，可使用《MindStudio Insight工具用户指南](https://www.hiascend.com/document/detail/zh/mindstudio/830/GUI_baseddevelopmenttool/msascendinsightug/Insight_userguide_0002.html)[》工具进行性能数据的查看和分析，如需了解详细字段解释请参见MindSpore&PyTorch框架性能数据文件参考](atlasprofiling_16_0203.html#ZH-CN_TOPIC_0000002536038401)。

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
```

```
└── msprof_1784298_20250620085947065_ascend_pt
    ├── ASCEND_PROFILER_OUTPUT
    │   ├── ascend_pytorch_profiler_{Rank_ID}.db    # 仅Atlas A3 训练系列产品/Atlas A3 推理系列产品、Atlas A2 训练系列产品/Atlas A2 推理系列产品支持默认导出该文件
    │   ├── kernel_details.csv
    │   ├── operator_details.csv
    │   ├── step_trace_time.csv
    │   └── trace_view.json
    ├── FRAMEWORK
...
    ├── PROF_000001_20250620085947066_FLRBJLNFMBIDRPMB
    │   ├── device_1
    │   │   ├── data
...
    │   ├── host
    │   │   ├── data
...
    │   ├── mindstudio_profiler_log
    │   └── mindstudio_profiler_output
    │       ├── api_statistic_20250620085954.csv
    │       ├── msprof_20250620085953.json
    │       ├── op_summary_20250620085954.csv
    │       ├── README.txt
    │       └── task_time_20250620085954.csv
    ├── profiler_info.json
    └── profiler_metadata.json

```
|  |  |
| --- | --- |