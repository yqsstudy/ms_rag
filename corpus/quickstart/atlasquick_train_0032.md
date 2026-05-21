---
title: "性能数据采集"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/msquickstart/atlasquick_train_0032.html"
date_collected: "2026-05-04"
category: "quickstart"
original_path: "zh/mindstudio/830/msquickstart/atlasquick_train_0032.html"
---

# 性能数据采集

#### 前提条件

- [完成环境准备](atlasquick_train_0002.html#ZH-CN_TOPIC_0000002502572164__section68892049173411)。
- [完成模型开发&迁移](atlasquick_train_0020.html)中的PyTorch部分，得到可正常执行训练任务的GPU和昇腾NPU环境。

[在执行性能数据采集前请先将训练脚本（pytorch_main.py文件）中的精度数据采集](atlasquick_train_0025.html)精度数据采集相关接口删除，因为精度数据采集和性能数据采集不可同时执行。

#### 执行采集

1. 在昇腾NPU环境下的训练脚本（pytorch_main.py文件）中添加Ascend PyTorch Profiler接口工具，如下所示。[在Ascend PyTorch Profiler接口采集性能数据代码样例](atlasquick_train_0036.html#ZH-CN_TOPIC_0000002534492005__section1294013163220)中插入如下代码，样例中已插入下列代码，可直接复制代码使用。
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
```

```
 23
 24 import torch_npu
 25 from torch_npu.contrib import transfer_to_npu
 26
...
318     model.train()

320     end = time.time()
321     experimental_config = torch_npu.profiler._ExperimentalConfig(
322         profiler_level=torch_npu.profiler.ProfilerLevel.Level0,
323         data_simplification=False)
324     with torch_npu.profiler.profile(
325         activities=[
326             torch_npu.profiler.ProfilerActivity.CPU,
327             torch_npu.profiler.ProfilerActivity.NPU
328             ],
329         schedule=torch_npu.profiler.schedule(wait=0, warmup=0, active=1, repeat=1, skip_first=1),
330         on_trace_ready=torch_npu.profiler.tensorboard_trace_handler("./profiling_data"),
331         experimental_config=experimental_config) as prof:
332         for i, (images, target) in enumerate(train_loader):
...
355             # measure elapsed time
356             batch_time.update(time.time() - end)
357             end = time.time()
358
359             prof.step()
...

```
|  |  |
| --- | --- |

  - [以上仅提供简单示例，若需要配置更完整的采集参数以及对应接口详细介绍请参见《性能调优工具用户指南](https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0001.html)[》中的“Ascend PyTorch调优工具](https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0121.html)”。
  - 性能数据会占据一定的磁盘空间，可能存在磁盘写满导致服务器不可用的风险。性能数据所需空间跟模型的参数、采集开关配置、采集的迭代数量有较大关系，须用户自行保证落盘目录下的可用磁盘空间。

2. 执行训练脚本命令，工具会采集模型训练过程中的性能数据。********
```
python pytorch_main.py -a resnet50 -b 32 --gpu 1 --dummy
```

3. 查看采集到的PyTorch训练性能数据结果文件。
**训练结束后，在torch_npu.profiler.tensorboard_trace_handler**接口指定的目录下生成Ascend PyTorch Profiler接口的性能数据结果目录，如下示例。

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
```

```
└── msprof_1784298_20250620085947065_ascend_pt
    ├── ASCEND_PROFILER_OUTPUT
    │   ├── ascend_pytorch_profiler_{Rank_ID}.db
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
...
    │   ├── msprof_*.db
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

[Ascend PyTorch Profiler接口采集的性能数据可以使用mstt的msprof-analyze工具进行辅助分析，也可以直接使用MindStudio Insight工具进行可视化分析，详细操作请参见使用msprof-analyze工具分析性能数据](atlasquick_train_0034.html)[和使用MindStudio Insight工具可视化性能数据](atlasquick_train_0035.html)。

**父主题：**[模型性能调优](atlasquick_train_0030.html)