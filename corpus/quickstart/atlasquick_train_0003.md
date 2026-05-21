---
title: "模型开发&amp;迁移"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/msquickstart/atlasquick_train_0003.html"
date_collected: "2026-05-04"
category: "quickstart"
original_path: "zh/mindstudio/830/msquickstart/atlasquick_train_0003.html"
---

# 模型开发&迁移

MindSpore训练场景暂未提供迁移工具，本文以直接在昇腾环境开发的训练脚本为例。

#### 前提条件

1. [完成环境准备](atlasquick_train_0002.html#ZH-CN_TOPIC_0000002502572164__section68892049173411)。
2. [以“mindspore_main.py”命名为例，创建训练脚本文件，脚本内容直接拷贝MindSpore昇腾NPU环境训练脚本样例](atlasquick_train_0019.html#ZH-CN_TOPIC_0000002534492001__section15254152515714)。
3. 将“mindspore_main.py”文件上传至训练服务器的任意目录下（需保证该目录下文件的读写权限）。

#### 执行训练

直接执行训练。
****
```
python mindspore_main.py
```

如果训练正常进行，完成后打印如下日志。

```
1
```

```
train finish

```
|  |  |
| --- | --- |
**父主题：**[训练场景工具快速入门](tools_qucikstart_0002.html)