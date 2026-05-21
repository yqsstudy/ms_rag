---
title: "性能数据采集"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/msquickstart/atlasquick_train_0015.html"
date_collected: "2026-05-04"
category: "quickstart"
original_path: "zh/mindstudio/830/msquickstart/atlasquick_train_0015.html"
---

# 性能数据采集

#### 前提条件

- [完成环境准备](atlasquick_train_0002.html#ZH-CN_TOPIC_0000002502572164__section68892049173411)。
- [根据模型开发&迁移](atlasquick_train_0003.html)中的MindSpore部分，完成MindSpore场景的训练任务。

[在执行性能数据采集前请先将训练脚本（mindspore_main.py文件）中的精度数据采集](atlasquick_train_0008.html)相关接口删除，因为精度数据采集和性能数据采集不可同时执行。

#### 执行采集

采集动作主要以MindSpore 2.7.0版本为例，若需要进行性能比对操作，也可以再采集MindSpore 2.6.0版本的性能数据。

1. 在昇腾NPU环境下的训练脚本（mindspore_main.py文件）中添加MindSpore Profiler接口工具，如下所示。[在MindSpore Profiler接口采集性能数据代码样例](atlasquick_train_0019.html#ZH-CN_TOPIC_0000002534492001__section1294013163220)中插入如下代码，样例中已插入下列代码，可直接复制代码使用。
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
```

```
 ...
from mindspore.profiler import ProfilerLevel, ProfilerActivity, AicoreMetrics
...
if __name__ == "__main__":
    mindspore.set_context(mode=mindspore.PYNATIVE_MODE)
    mindspore.set_device("Ascend")

    # Init Profiler
    experimental_config = mindspore.profiler._ExperimentalConfig(
        profiler_level=ProfilerLevel.Level0,
        aic_metrics=AicoreMetrics.AiCoreNone,
        l2_cache=False,
        mstx=False,
        data_simplification=False,
    )

    step = 0
    # Note that the Profiler should be initialized before model.train
    with mindspore.profiler.profile(
            activities=[ProfilerActivity.CPU, ProfilerActivity.NPU],
            schedule=mindspore.profiler.schedule(
                wait=0, warmup=0, active=1, repeat=1, skip_first=0
            ),
            on_trace_ready=mindspore.profiler.tensorboard_trace_handler("./profiling_data"),
            profile_memory=False,
            experimental_config=experimental_config,
    ) as prof:
        # Train Model
        for data, label in ds.GeneratorDataset(generator_net(), ["data", "label"]):
            train_step(data, label)
            print(f"train step {step}")
            step += 1
            prof.step()
        print("train finish")

```
|  |  |
| --- | --- |

  - [以上仅提供简单示例，若需要配置更完整的采集参数以及对应接口详细介绍请参见《mindspore.profiler.profile](https://www.mindspore.cn/docs/zh-CN/r2.6.0/api_python/mindspore/mindspore.profiler.profile.html)》。
  - 性能数据会占据一定的磁盘空间，可能存在磁盘写满导致服务器不可用的风险。性能数据所需空间跟模型的参数、采集开关配置、采集的迭代数量有较大关系，须用户自行保证落盘目录下的可用磁盘空间。

2. 执行训练脚本命令，工具会采集模型训练过程中的性能数据。**
```
python mindspore_main.py
```

3. 查看采集到的MindSpore训练性能数据结果文件。
**训练结束后，在mindspore.profiler.****tensorboard_trace_handler**接口指定的目录下生成MindSpore Profiler接口的性能数据结果目录，如下示例。

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
└── msprof_1198203_20250617064811905_ascend_ms
├── ASCEND_PROFILER_OUTPUT
│   ├── api_statistic.csv
│   ├── dataset.csv
│   ├── kernel_details.csv
│   ├── step_trace_time.csv
│   └── trace_view.json
├── FRAMEWORK
...
├── PROF_000001_20250617064812088_QGGJHHNAODRDOJFB
│   ├── device_0
│   │   ├── data
...
│   ├── host
│   │   ├── data
...
│   ├── mindstudio_profiler_log
...
│   └── mindstudio_profiler_output
│       ├── api_statistic_20250617064814.csv
│       ├── msprof_20250617064813.json
│       ├── op_summary_20250617064814.csv
│       ├── README.txt
│       └── task_time_20250617064814.csv
└── profiler_info_0.json

```
|  |  |
| --- | --- |

[MindSpore Profiler接口采集的性能数据可以使用mstt的msprof-analyze工具进行辅助分析，也可以直接使用MindStudio Insight工具进行可视化分析，详细操作请参见使用msprof-analyze工具分析性能数据](atlasquick_train_0017.html)[和使用MindStudio Insight工具可视化性能数据](atlasquick_train_0018.html)。

**父主题：**[模型性能调优](atlasquick_train_0013.html)