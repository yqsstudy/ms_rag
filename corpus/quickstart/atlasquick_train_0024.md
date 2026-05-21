---
title: "训练状态监控"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/msquickstart/atlasquick_train_0024.html"
date_collected: "2026-05-04"
category: "quickstart"
original_path: "zh/mindstudio/830/msquickstart/atlasquick_train_0024.html"
---

# 训练状态监控

#### 前提条件

- [完成环境准备](atlasquick_train_0002.html#ZH-CN_TOPIC_0000002502572164__section68892049173411)。
- [完成训练前配置检查](atlasquick_train_0023.html)。

#### 操作步骤

1. 以执行权重梯度监控功能为例，创建配置文件。
以在训练脚本所在目录创建monitor_config.json配置文件为例，文件内容拷贝如下示例配置。

```
1
2
3
4
5
6
7
```

```
{ 
    "targets": {
    },
    "wg_distribution": true,
    "format": "csv",
    "ops": ["norm", "min", "max", "nans"]
} 

```
|  |  |
| --- | --- |

2. 在训练脚本中添加工具，如下所示。
[在PyTorch训练状态监控代码样例](atlasquick_train_0036.html#ZH-CN_TOPIC_0000002534492005__section17304535155919)中插入如下代码，样例中已插入下列代码，可直接复制代码使用。

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
```

```
 23
 24 import torch_npu
 25 from torch_npu.contrib import transfer_to_npu
 26 
 27 monitor = TrainerMon(
 28     config_file_path="./monitor_config.json",
 29     params_have_main_grad=False,  # 权重是否使用main_grad，通常megatron为True，deepspeed为False。默认为True。
 30 ) 
...
333     # switch to train mode
334     model.train()
335 
336     # 挂载监控对象
337     monitor.set_monitor(
338         model,
339         grad_acc_steps=1,
340         optimizer=optimizer,
341         dp_group=None,
342         tp_group=None,
343         start_iteration=0  # 断点续训时提供当前iteration，默认从0开始
344     ) 
...

```
|  |  |
| --- | --- |

3. 执行训练脚本命令。********
```
python pytorch_main.py -a resnet50 -b 32 --gpu 1 --dummy
```

4. 查看结果。**训练执行完成后在当前路径生成monitor_output目录，目录下根据时间戳生成多份结果，查看最新目录下的文件，如下所示。图1**
结果文件内容
[输出结果详细介绍请参见“输出路径](https://gitcode.com/Ascend/mstt/blob/br_release_MindStudio_8.3.0_20261231/debug/accuracy_tools/msprobe/docs/19.monitor.md#输出路径)”。

**父主题：**[模型精度调试](atlasquick_train_0021.html)