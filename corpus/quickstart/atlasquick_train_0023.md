---
title: "训练前配置检查"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/msquickstart/atlasquick_train_0023.html"
date_collected: "2026-05-04"
category: "quickstart"
original_path: "zh/mindstudio/830/msquickstart/atlasquick_train_0023.html"
---

# 训练前配置检查

根据本手册的样例，需要将工具接口添加到训练脚本中进行配置检查。

需要在GPU和昇腾NPU环境上分别执行检查。

#### 前提条件

- [完成环境准备](atlasquick_train_0002.html#ZH-CN_TOPIC_0000002502572164__section68892049173411)。
- [完成模型开发&迁移](atlasquick_train_0020.html)，确保在所有示例的环境可正常完成训练任务。

#### 环境准备

在昇腾NPU环境下安装msprobe工具，执行如下命令：

```
pip install mindstudio-probe
```

#### 执行检查

操作步骤如下：

1. 获取两个环境的zip包（包含影响训练精度的环境配置：环境变量、第三方库版本、训练超参、权重、数据集、随机操作）。
分别在GPU和昇腾NPU环境下执行以下操作。需要注意给两个zip包不同的命名。

[在PyTorch训练前配置检查代码样例](atlasquick_train_0036.html#ZH-CN_TOPIC_0000002534492005__section6244318903)中插入如下代码，样例中已插入下列代码，可直接复制代码使用。

  1. 在训练流程执行到的第一个Python脚本开始处插入如下代码。
```
1
2
```

```
  1 from msprobe.core.config_check import ConfigChecker
  2 ConfigChecker.apply_patches(fmk)

```
|  |  |
| --- | --- |

fmk：训练框架，string类型，可选"pytorch"和"mindspore"，这里配置为"pytorch"。

  2. 在模型初始化好之后插入如下代码。
```
1
2
```

```
172 from msprobe.core.config_check import ConfigChecker
173 ConfigChecker(model, output_zip_path, fmk)

```
|  |  |
| --- | --- |

    - model：初始化好的模型，默认不会采集权重和数据集。
    - output_zip_path：输出zip包的路径，string类型，需要指定zip包的名称，默认为"./config_check_pack.zip"。
    - fmk：训练框架。可选"pytorch"和"mindspore"，这里配置为"pytorch"。

  3. 执行训练脚本命令。********
```
python pytorch_main.py -a resnet50 -b 32 --gpu 1 --dummy
```

采集完成后会得到一个zip包，里面包括各项影响精度的配置。分rank和step存储，其中step为micro_step。

2. 将两个zip包传到同一个环境下，使用如下命令进行比对。********
```
msprobe -f pytorch config_check -c bench_zip_path cmp_zip_path -o output_path 
```

其中bench_zip_path为标杆侧采集到的zip包名称，cmp_zip_path为待对比侧采集到的zip包名称。

output_path默认为"./config_check_result"。

执行以上命令后，在output_path里会生成如下数据：

  - bench：bench_zip_path里打包的数据。
  - cmp：cmp_zip_path里打包的数据。
  - result.xlsx：比对结果。会有多个sheet页，其中summary总览通过情况，其余页是具体检查项的详情，其中step为micro_step。

3. 检查通过情况。两个环境以下五项检查均一致则通过，若不一致则需要自行调整环境：
  - 环境变量
  - 第三方库版本
  - 数据集
  - 权重
  - 训练超参

如下所示：

```
1
2
3
4
5
6
```

```
filename    ass_check
env         TRUE
pip	    TRUE
dataset     TRUE
weights     TRUE
random      TRUE

```
|  |  |
| --- | --- |

**父主题：**[模型精度调试](atlasquick_train_0021.html)