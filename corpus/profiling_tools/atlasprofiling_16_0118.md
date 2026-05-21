---
title: "性能数据采集和自动解析"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0118.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0118.html"
---

# 性能数据采集和自动解析

MindSpore Profiler是针对MindSpore框架开发的性能分析工具，通过在MindSpore训练脚本中添加MindSpore Profiler接口，执行训练的同时采集性能数据，完成训练后直接输出可视化的性能数据文件，提升了性能分析效率。MindSpore Profiler接口可全面采集MindSpore训练场景下的性能数据，主要包括MindSpore层算子信息、CANN层算子信息、底层NPU算子信息、以及算子内存占用信息等，可以全方位分析MindSpore训练时的性能状态。

MindSpore场景当前支持如下性能数据采集方式：

- mindspore.profiler.profile接口采集
提供完整的采集接口，通过在代码中添加接口，可以自由选择采集的内容。

- mindspore.profiler.DynamicProfilerMonitor动态采集
支持在训练过程中随时启动采集，采集时间更灵活。

- 环境变量采集
支持不修改用户代码直接启动采集，采集方式更简便。

- msprof命令行采集（非MindSpore Profiler接口）
通用的采集方式，支持不修改用户代码直接启动采集，采集方式更简便。

MindSpore 2.0及之后的版本支持。

#### 约束

MindSpore Profiler接口支持多种采集方式，各采集方式不可同时开启。

须保证MindSpore Profiler接口的调用与要采集的业务流程在同一个进程内。

MindSpore Profiler接口进行采集任务时，进程与Device之间的关系如下：

- 多进程多Device场景：支持每个Device下分别设置一个采集进程。
- 单进程多Device场景：不支持。
- 多进程单Device场景：需要保证多进程之间的采集动作是串行的，即各个采集动作不在同一时间开始，且各个采集动作须包含完整的启动和停止。

#### 前提条件

- [请确保完成使用前准备](atlasprofiling_16_0002.html#ZH-CN_TOPIC_0000002504358330)。
- 准备好基于MindSpore 2.7.0版本开发的训练模型以及配套的数据集，完成训练脚本（如train_*.py）开发并在昇腾AI处理器环境下正常训练。

#### mindspore.profiler.profile接口采集

该接口支持两种采集方式：Callback方式和自定义for循环方式，且在Graph和PyNative两种模式下都支持。

[接口详细介绍请参见调试调优](https://www.mindspore.cn/docs/zh-CN/master/api_python/mindspore.html#调试调优)。

1. 在训练脚本内添加如下示例代码进行性能数据采集参数配置，之后启动训练。

  - Callback方式采集样例
[完整案例请参见call_back_profiler](https://gitee.com/mindspore/docs/blob/master/docs/sample_code/profiler/call_back_profiler.py)。

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
import mindspore

class StopAtStep(mindspore.Callback):
    def __init__(self, start_step, stop_step):
        super(StopAtStep, self).__init__()
        self.start_step = start_step
        self.stop_step = stop_step
        experimental_config = mindspore.profiler._ExperimentalConfig()
        self.profiler = mindspore.profiler.profile(start_profile=False, experimental_config=experimental_config,
                                                   schedule=mindspore.profiler.schedule(wait=0, warmup=0, active=self.stop_step - self.start_step + 1, repeat=1, skip_first=0),
                                                   on_trace_ready=mindspore.profiler.tensorboard_trace_handler("./data"))

    def on_train_step_begin(self, run_context):
        cb_params = run_context.original_args()
        step_num = cb_params.cur_step_num
        if step_num == self.start_step:
            self.profiler.start()

    def on_train_step_end(self, run_context):
        cb_params = run_context.original_args()
        step_num = cb_params.cur_step_num
        if self.start_step <= step_num <= self.stop_step:
            self.profiler.step()
        if step_num == self.stop_step:
            self.profiler.stop()

```
|  |  |
| --- | --- |

  - 自定义for循环方式采集样例
自定义for循环方式下，用户可以通过设置schedule以及on_trace_ready参数来启动Profiler。

例如用户想要采集前两个step的性能数据，可以使用如下配置的schedule进行采集。

[完整案例参见for_loop_profiler](https://gitee.com/mindspore/docs/blob/master/docs/sample_code/profiler/for_loop_profiler.py)。

```
import mindspore
from mindspore.profiler import ProfilerLevel, ProfilerActivity, AicoreMetrics

# 定义模型训练次数
steps = 15

# 定义训练模型网络
net = Net()

# 配置可扩展参数
experimental_config = mindspore.profiler._ExperimentalConfig(
                        profiler_level=ProfilerLevel.Level0,
                        aic_metrics=AicoreMetrics.AiCoreNone,
                        l2_cache=False,
                        mstx=False,
                        data_simplification=False)

# 初始化profile
with mindspore.profiler.profile(activities=[ProfilerActivity.CPU, ProfilerActivity.NPU],
                                    schedule=mindspore.profiler.schedule(wait=1, warmup=1, active=2,
                                            repeat=1, skip_first=2),
                                    on_trace_ready=mindspore.profiler.tensorboard_trace_handler("./data"),
                                    profile_memory=False,
                                    experimental_config=experimental_config) as prof:
        for step in range(steps):
            train(net)
            # 调用step采集
            prof.step()
```

2. 性能数据解析。

[支持自动解析（参照以上示例代码中tensorboard_trace_handler](https://www.mindspore.cn/docs/zh-CN/master/api_python/mindspore/mindspore.profiler.tensorboard_trace_handler.html#mindspore.profiler.tensorboard_trace_handler)[）和离线解析](atlasprofiling_16_0119.html#ZH-CN_TOPIC_0000002536038351)。

3. 查看性能数据结果文件和性能数据分析。

[性能数据结果文件详细介绍请参见MindSpore&PyTorch框架性能数据文件参考](atlasprofiling_16_0203.html#ZH-CN_TOPIC_0000002536038401)。

[请参见《MindStudio Insight工具用户指南](https://www.hiascend.com/document/detail/zh/mindstudio/830/GUI_baseddevelopmenttool/msascendinsightug/Insight_userguide_0002.html)》将解析后的性能数据文件进行可视化展示和分析。

[可以使用性能分析工具（msprof-analyze）](https://gitcode.com/Ascend/mstt/tree/master/profiler/msprof_analyze)辅助分析性能数据。

#### mindspore.profiler.DynamicProfilerMonitor动态采集

在训练过程中，如果用户想要在不中断训练流程的前提下，修改配置文件并完成新配置下的采集任务，可以使用mindspore.profiler.DynamicProfilerMonitor接口。该接口需要配置一个json文件，该json文件的命名必须为“profiler_config.json”，如果不配置则会生成一个默认的json配置文件。

[mindspore.profiler.DynamicProfilerMonitor接口及json配置文件参数详细介绍，请参见mindspore.profiler.DynamicProfilerMonitor](https://www.mindspore.cn/docs/zh-CN/master/api_python/mindspore/mindspore.profiler.DynamicProfilerMonitor.html)。

1. 创建“profiler_config.json”配置文件，示例如下。

```
{
   "start_step": 2,
   "stop_step": 5,
   "aic_metrics": -1,
   "profiler_level": 0,
   "activities": 0,
   "export_type": 0,
   "profile_memory": false,
   "mstx": false,
   "analyse": true,
   "analyse_mode": 0,
   "parallel_strategy": false,
   "with_stack": false,
   "data_simplification": true
}
```

2. 在训练脚本内添加如下示例代码进行性能数据采集参数配置，之后启动训练。
[完整案例请参见dynamic_profiler](https://gitee.com/mindspore/docs/blob/master/docs/sample_code/profiler/dynamic_profiler.py)。
```
from mindspore.profiler import DynamicProfilerMonitor

# cfg_path中包括上述的json配置文件路径，output_path为输出路径
dp = DynamicProfilerMonitor(cfg_path="./cfg_path", output_path="./output_path")
STEP_NUM = 15
# 定义训练模型网络
net = Net()
for _ in range(STEP_NUM):
    train(net)
    # 调用step采集
    dp.step()
```

3. 性能数据解析。

[支持自动解析（配置文件的"analyse"参数控制）和离线解析](atlasprofiling_16_0119.html#ZH-CN_TOPIC_0000002536038351)。

4. 查看性能数据结果文件和性能数据分析。

[性能数据结果文件详细介绍请参见MindSpore&PyTorch框架性能数据文件参考](atlasprofiling_16_0203.html#ZH-CN_TOPIC_0000002536038401)。

[请参见《MindStudio Insight工具用户指南](https://www.hiascend.com/document/detail/zh/mindstudio/830/GUI_baseddevelopmenttool/msascendinsightug/Insight_userguide_0002.html)》将解析后的性能数据文件进行可视化展示和分析。

[可以使用性能分析工具（msprof-analyze）](https://gitcode.com/Ascend/mstt/tree/master/profiler/msprof_analyze)辅助分析性能数据。

#### 环境变量采集

将参数配置到MS_PROFILER_OPTIONS环境变量中，在模型训练中会自动采集性能数据。

[环境变量详细参数介绍请参见环境变量](https://www.mindspore.cn/docs/zh-CN/master/api_python/env_var_list.html#profiler)。

- 该方式只支持单卡场景。
- 该方式暂不支持schedule、on_trace_ready、experimental_config参数。
- 请在训练脚本开始执行前通过环境变量设置好device_id。不支持在训练脚本中通过set_context函数设置device_id。

1. 配置环境变量，如下示例。

```
export MS_PROFILER_OPTIONS='
{"start": true,
"output_path": "./output_path",
"activities": ["CPU", "NPU"],
"with_stack": true,
"aic_metrics": "AicoreNone",
"l2_cache": false,
"profiler_level": "Level0"}'
```

其中"start"须配置为true，才能启动采集。

2. 启动训练脚本完成采集。
3. 性能数据解析。

[支持自动解析和离线解析](atlasprofiling_16_0119.html#ZH-CN_TOPIC_0000002536038351)。

4. 查看性能数据结果文件和性能数据分析。

[性能数据结果文件详细介绍请参见MindSpore&PyTorch框架性能数据文件参考](atlasprofiling_16_0203.html#ZH-CN_TOPIC_0000002536038401)。

[请参见《MindStudio Insight工具用户指南](https://www.hiascend.com/document/detail/zh/mindstudio/830/GUI_baseddevelopmenttool/msascendinsightug/Insight_userguide_0002.html)》将解析后的性能数据文件进行可视化展示和分析。

[可以使用性能分析工具（msprof-analyze）](https://gitcode.com/Ascend/mstt/tree/master/profiler/msprof_analyze)辅助分析性能数据。

#### msprof命令行采集

MindSpore 2.0或更高版本支持通过msprof命令行方式进行性能数据采集。

[msprof命令行详细参数介绍请参见性能数据采集和自动解析](atlasprofiling_16_0007.html#ZH-CN_TOPIC_0000002536038281)。

1. 执行msprof命令启动采集，如下示例。
****
```
msprof --output=./output_path python3 ./train_*.py
```

*“**python3 ./train_*.py”*为训练执行命令，须在msprof命令行及参数的末尾添加。

*完成采集后在--output参数指定目录下生成“PROF_*XXX”目录。

2. 性能数据解析。

*“PROF_*[XXX”目录下的“mindstudio_profiler_output”目录为自动解析后的性能数据，若需要手动解析请参见离线解析](atlasprofiling_16_0015.html#ZH-CN_TOPIC_0000002536038287)。

3. 查看性能数据结果文件和性能数据分析。

[性能数据结果文件详细介绍请参见MindSpore&PyTorch框架性能数据文件参考](atlasprofiling_16_0203.html#ZH-CN_TOPIC_0000002536038401)。

[请参见《MindStudio Insight工具用户指南](https://www.hiascend.com/document/detail/zh/mindstudio/830/GUI_baseddevelopmenttool/msascendinsightug/Insight_userguide_0002.html)》将解析后的性能数据文件进行可视化展示和分析。

[可以使用性能分析工具（msprof-analyze）](https://gitcode.com/Ascend/mstt/tree/master/profiler/msprof_analyze)辅助分析性能数据。

**父主题：**[MindSpore调优工具](atlasprofiling_16_0117.html)