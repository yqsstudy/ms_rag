---
title: "精度数据采集"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/msquickstart/atlasquick_train_0008.html"
date_collected: "2026-05-04"
category: "quickstart"
original_path: "zh/mindstudio/830/msquickstart/atlasquick_train_0008.html"
---

# 精度数据采集

#### 前提条件

- [完成环境准备](atlasquick_train_0002.html#ZH-CN_TOPIC_0000002502572164__section68892049173411)。
- [完成训练前配置检查](atlasquick_train_0006.html)。

#### 执行采集

1. 创建配置文件。以在训练脚本所在目录创建config.json配置文件为例，文件内容拷贝如下示例配置。
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
```

```
{
    "task": "tensor",
    "dump_path": "./dump_data",
    "rank": [],
    "step": [],
    "level": "L1",

    "tensor": {
        "scope": [], 
        "list": [],
        "data_mode": ["all"]
    }
}

```
|  |  |
| --- | --- |

2. 在训练脚本（mindspore_main.py文件）中添加工具，如下所示。[在MindSpore精度数据采集代码样例](atlasquick_train_0019.html#ZH-CN_TOPIC_0000002534492001__section9888111810483)中插入如下代码，样例中已插入下列代码，可直接复制代码使用。
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
```

```
...
  8 from msprobe.mindspore import PrecisionDebugger
  9 debugger = PrecisionDebugger(config_path="./config.json")
...
 47 if __name__ == "__main__":
 48     step = 0
 49     # Train Model
 50     for data, label in ds.GeneratorDataset(generator_net(), ["data", "label"]):
 51         debugger.start(model)
 52         train_step(data, label)
 53         print(f"train step {step}")
 54         step += 1
 55         debugger.stop()
 56         debugger.step()
 57     print("train finish")

```
|  |  |
| --- | --- |

精度数据会占据一定的磁盘空间，可能存在磁盘写满导致服务器不可用的风险。精度数据所需空间跟模型的参数、采集开关配置、采集的迭代数量有较大关系，须用户自行保证落盘目录下的可用磁盘空间。

3. 执行训练脚本命令，工具会采集模型训练过程中的精度数据。**
```
python mindspore_main.py
```

日志打印出现如下示例信息表示数据采集成功，完成采集后即可查看数据。

```
1
2
3
4
5
```

```
The cell hook function is successfully mounted to the model.
The module statistics hook function is successfully mounted to the model.
msprobe: debugger.start() is set successfully
Dump switch is turned on at step 0.
Dump data will be saved in /home/user1/dump/dump_data/step0.

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
        │   ├── Jit.Momentum.0.forward.input.1.0.npy
        │   ├── Primitive.matmul.MatMul.1.forward.input.1.npy
        │   ├── Mint.add.1.backward.input.0.npy
        │   ├── Primitive.matmul.MatMul.1.forward.output.0.npy
        ...
        └── stack.json               # 保存API的调用栈信息
├── step1
...

```
|  |  |
| --- | --- |

[采集后的数据需要用精度预检](atlasquick_train_0009.html)[和精度比对](atlasquick_train_0010.html)等工具进行进一步分析。
**父主题：**[模型精度调试](atlasquick_train_0004.html)