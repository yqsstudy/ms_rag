---
title: "set_flag"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdevapi_16_00073.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdevapi_16_00073.html"
---

# set_flag

#### 功能说明

[用于确保核内各PIPE间不同指令的同步，pipe_src先完成调度后，pipe_dst将解除阻塞状态。设置set_flag和wait_flag](atlasopdevapi_16_00074.html)[之后，指令流水图介绍（以MindStudio Insight为例）](https://www.hiascend.com/document/detail/zh/mindstudio/82RC1/ODtools/Operatordevelopmenttools/atlasopdev_16_0087.html)将会更贴合用户的调用预期。

#### 接口原型

```
1
```

```
set_flag(pipe_src, pipe_dst, event_id)

```
|  |  |
| --- | --- |

#### 参数说明

参数名

输入/输出

说明

pipe_src

输入

源PIPE，在pipe_src调度后设置event_id。

[输入格式为aicore_PIPE，例如："aic0_PIPE-MTE1"。其中aicore的取值范围参见基础功能接口Core](atlasopdevapi_16_0004.html)，PIPE取值范围为"PIPE-MTE1"、"PIPE-MTE2"、 "PIPE-MTE3"、"PIPE-FIX"、"PIPE-M"、"PIPE-V"、 "PIPE-S"。不指定aicore时，可直接输入PIPE取值。

数据类型：string。

必选参数。

pipe_dst

输入

目的PIPE，在pipe_src调度之后，pipe_dst将会解除阻塞状态。

[输入格式为aicore_PIPE，例如："aic0_PIPE-MTE1"。其中aicore的取值范围参见基础功能接口Core](atlasopdevapi_16_0004.html)，PIPE取值范围为"PIPE-MTE1"、"PIPE-MTE2"、 "PIPE-MTE3"、"PIPE-FIX"、"PIPE-M"、"PIPE-V"、 "PIPE-S"。不指定aicore时，可直接输入PIPE取值。

数据类型：string。

必选参数。

event_id

输入

同步指令之间依赖的唯一值。

取值范围[0, 65535]。

数据类型：int。

必选参数。
|  |  |  |
| --- | --- | --- |
|  |  |  |
|  |  |  |
|  |  |  |

#### 约束说明

- 在同一核内set_flag与wait_flag个数需匹配。
- 同核内不应出现重复的set_flag指令。
- 同一核内，当set_flag和wait_flag内的pipe_src和pipe_dst相同时，event_id也应保持唯一。

#### 使用示例

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
from mskpp import Tensor, Chip, set_flag, wait_flag
with Chip("Ascendxxyy") as chip:
    gm_weight = Tensor("GM", "FP16", [128, 256], format="ND")
    l1_weight = Tensor("L1", "FP16", [128, 256], format="ND")
    for conv_idx in range(4):  # L0A数据加载前，GM分批加载到L1上
        gm_weight_part = gm_weight[:, 64]
        l1_weight_part = l1_weight[:, 64]
        l1_weight_part.load(gm_weight_part)
        if conv_idx == 3:
            set_flag("PIPE-MTE2", "PIPE-MTE1", 1)  # 当完成MTE2，才可以执行MTE1
    x = Tensor("L0A")   # L0A
    # 正在执行MTE2操作， MTE1操作需要等待MTE2完成才能执行。
    l1_weight.set_valid()  # 手动使能L1
    wait_flag("PIPE-MTE2", "PIPE-MTE1", 1)
    x.load(l1_weight)

```
|  |  |
| --- | --- |
**父主题：**[同步类指令接口](atlasopdevapi_16_00072.html)