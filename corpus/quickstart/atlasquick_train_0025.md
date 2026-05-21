---
title: "精度数据采集"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/msquickstart/atlasquick_train_0025.html"
date_collected: "2026-05-04"
category: "quickstart"
original_path: "zh/mindstudio/830/msquickstart/atlasquick_train_0025.html"
---

# 精度数据采集

本样例选用ResNet50模型，采用虚拟数据训练，节省数据集下载时间。

#### 前提条件

- [完成环境准备](atlasquick_train_0002.html#ZH-CN_TOPIC_0000002502572164__section68892049173411)。
- [完成训练前配置检查](atlasquick_train_0023.html)。

#### 执行采集

1. 分别在GPU和昇腾NPU环境下的训练脚本（pytorch_main.py文件）中添加工具，如下所示。
其中在GPU环境下执行训练时，下列脚本中不需要添加24、25行。
[在PyTorch精度数据采集代码样例](atlasquick_train_0036.html#ZH-CN_TOPIC_0000002534492005__section1190213460591)中插入如下代码，样例中已插入下列代码，可直接复制代码使用。
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
 27 from msprobe.pytorch import PrecisionDebugger, seed_all
 28 seed_all(seed=1234, mode=True)    # 固定随机种子，开启确定性计算，保证每次模型执行数据均保持一致
...
314 def train(train_loader, model, criterion, optimizer, epoch, device, args):
...
331     end = time.time()
332
333     debugger = PrecisionDebugger(dump_path="./dump_data", task="tensor", step=[0, 1])
334     for i, (images, target) in enumerate(train_loader):
335         debugger.start()
...
356
357         # measure elapsed time
358         batch_time.update(time.time() - end)
359         end = time.time()
360
361         debugger.stop()
362         debugger.step()

```
|  |  |
| --- | --- |

精度数据会占据一定的磁盘空间，可能存在磁盘写满导致服务器不可用的风险。精度数据所需空间跟模型的参数、采集开关配置、采集的迭代数量有较大关系，须用户自行保证落盘目录下的可用磁盘空间。

2. 执行训练脚本命令，工具会采集模型训练过程中的精度数据。********
```
python pytorch_main.py -a resnet50 -b 32 --gpu 1 --dummy
```

日志打印出现如下信息即可手动停止模型训练查看采集数据，节省时间。

```
1
2
3
```

```
****************************************************************************
*                        msprobe ends successfully.                        *
****************************************************************************

```
|  |  |
| --- | --- |

#### 结果查看

dump_path参数指定的路径下会出现如下目录结构，可以根据需求选择合适的数据进行分析。

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
```

```
dump_data/
├── step0
    └── rank
        ├── construct.json           # 保存Module的层级关系信息，当前场景为空
        ├── dump.json                # 保存前反向API的输入输出的统计量信息和溢出信息等
        ├── dump_tensor_data         # 保存前反向API的输入输出tensor的真实数据信息等
        │   ├── Functional.adaptive_avg_pool2d.0.backward.input.0.pt
        │   ├── Functional.adaptive_avg_pool2d.0.backward.output.0.pt
        │   ├── Functional.adaptive_avg_pool2d.0.forward.input.0.pt
        │   ├── Functional.adaptive_avg_pool2d.0.forward.output.0.pt
        ...
        └── stack.json               # 保存API的调用栈信息
├── step1
...

```
|  |  |
| --- | --- |

[采集后的数据需要用精度预检](atlasquick_train_0026.html)[和精度比对](atlasquick_train_0027.html)等工具进行进一步分析。
**父主题：**[模型精度调试](atlasquick_train_0021.html)