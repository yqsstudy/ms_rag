---
title: "模型开发&amp;迁移"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/msquickstart/atlasquick_train_0020.html"
date_collected: "2026-05-04"
category: "quickstart"
original_path: "zh/mindstudio/830/msquickstart/atlasquick_train_0020.html"
---

# 模型开发&迁移

PyTorch训练场景使用PyTorch GPU2Ascend工具，将基于GPU的训练脚本迁移为支持昇腾NPU环境的脚本，提高脚本迁移速度，降低开发者的工作量。本样例可以让开发者快速体验PyTorch GPU2Ascend工具的迁移效率。原基于GPU的训练脚本迁移成功后可在昇腾NPU环境上运行。

[PyTorch GPU2Ascend工具为分析迁移工具之一，更多介绍请参见《分析迁移工具用户指南](https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/MigrationTool/atlasfmkt_16_0001.html)》。

#### 前提条件

1. [完成环境准备](atlasquick_train_0002.html#ZH-CN_TOPIC_0000002502572164__section68892049173411)。
2. [本样例选用ResNet50模型，以“pytorch_main.py”命名为例，创建训练脚本文件，脚本内容直接拷贝PyTorch GPU环境训练脚本样例](atlasquick_train_0036.html#ZH-CN_TOPIC_0000002534492005__section16500231603)[（也可以下载main.py](https://gitcode.com/Ascend/mstt/blob/master/sample/transfer_to_npu/main.py)文件）。
3. 将“pytorch_main.py”文件上传至训练服务器的任意目录下（需保证该目录下文件的读写权限）。

#### 执行迁移

需要先将基于GPU的训练脚本迁移为支持昇腾NPU环境的脚本，再执行训练。

1. 在训练脚本（pytorch_main.py文件）中导入自动迁移的库代码。
[以PyTorch 昇腾NPU环境训练脚本样例](atlasquick_train_0036.html#ZH-CN_TOPIC_0000002534492005__section489123942720)为例。
```
1
2
3
4
5
```

```
 22
 23 import torch_npu
 24 from torch_npu.contrib import transfer_to_npu
 25
# 在23 24行插入的代码为自动迁移的库代码，可以在昇腾NPU环境下直接执行训练

```
|  |  |
| --- | --- |

2. 迁移完成后的训练脚本可在昇腾NPU环境上运行，执行以下训练命令。
********
```
python pytorch_main.py -a resnet50 -b 32 --gpu 1 --dummy
```

如果训练正常进行，开始打印迭代日志，说明训练功能迁移成功，如下所示。

```
1
2
3
4
5
6
```

```
Using device: npu
=> creating model 'resnet50'
=> Dummy data is used!
Epoch: [0][    1/40037] Time  4.923 ( 4.923)    Data  0.502 ( 0.502)    Loss 7.0165e+00 (7.0165e+00)    Acc@1   0.00 (  0.00)   Acc@5   0.00 (  0.00)
Epoch: [0][   11/40037] Time  0.061 ( 0.996)    Data  0.000 ( 0.541)    Loss 1.2860e+01 (1.9566e+01)    Acc@1   0.00 (  0.00)   Acc@5   0.00 (  0.85)
Epoch: [0][   21/40037] Time  0.063 ( 0.551)    Data  0.000 ( 0.285)    Loss 9.5061e+00 (1.5033e+01)    Acc@1   0.00 (  0.00)   Acc@5   0.00 (  0.74)

```
|  |  |
| --- | --- |

3. 成功保存权重，说明保存权重功能迁移成功。
**父主题：**[训练场景工具快速入门](tools_qucikstart_0002.html)