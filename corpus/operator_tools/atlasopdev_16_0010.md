---
title: "算子计算搬运规格分析"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0010.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0010.html"
---

# 算子计算搬运规格分析

*文档中的Ascendxxxyy*需替换为实际使用的处理器类型。
以matmul算子为例，该用例表示准备处理[160, 240]和[240, 80]的矩阵乘，切割为5个[32, 48]、[48, 16]和[32, 16]的小矩阵做矩阵乘。通过调用msKPP提供的接口实现的main.py脚本样例如下：
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
35
36
37
```

```
from mskpp import mmad, Tensor, Chip
def my_mmad(gm_x, gm_y, gm_z):
    # 矩阵乘的基本数据通路：
    # 左矩阵x：GM-L1-L0A
    # 右矩阵y：GM-L1-L0B
    # 结果矩阵z： L0C(初始化)-GM
    # 样例数学表达式：z = x @ y + b
    # 定义和分配L1上的变量
    l1_x = Tensor("L1")
    l1_y = Tensor("L1")
    # 定义和分配L0A和L0B上的变量
    x = Tensor("L0A")
    y = Tensor("L0B")
    # 定义和分配在L0C上的偏置项，理论上应该分配在累加器Buffer上，分配在L0C不影响性能
    b = Tensor("L0C", "FP32", [32, 16], format="NC1HWC0")
    # 将GM上的数据移动到L1对应内存空间上
    l1_x.load(gm_x)
    l1_y.load(gm_y)
    # 将L1上的左右矩阵移动到L0A和L0B上
    x.load(l1_x)
    y.load(l1_y)
    # 当前数据已加载到L0A和L0B上，调用指令进行计算，结果保存在L0C上，out是mmad函数内部在L0C中分配的变量
    out = mmad(x, y, b, True)()
    # 将L0C上的数据移动到GM变量gm_z的地址空间上
    gm_z.load(out[0])
    return gm_z
if __name__ == '__main__':
    with Chip("Ascendxxxyy") as chip:
        chip.enable_trace() # 使能算子模拟流水图的功能，生成trace.json文件
        chip.enable_metrics() # 使能单指令及分PIPE的流水信息，生成Instruction_statistic.csv和Pipe_statistic.csv文件
        # 模拟一个大矩阵被切分成5个小矩阵进行计算
        for _ in range(5):
            # 应用算子进行AICORE计算
            in_x = Tensor("GM", "FP16", [32, 48], format="ND")
            in_y = Tensor("GM", "FP16", [48, 16], format="ND")
            in_z = Tensor("GM", "FP32", [32, 16], format="NC1HWC0")
            my_mmad(in_x, in_y, in_z)

```
|  |  |
| --- | --- |

**使用Python执行以上main.py脚本后，会在当前路径/MSKPP*****TIMESTAMP***目录下生成搬运流水统计文件（Pipe_statistic.csv）和指令信息统计文件（Instruction_statistic.csv），可查看msKPP建模结果。

*TIMESTAMP*为当前时间戳。

#### 搬运流水统计
**搬运流水统计文件Pipe_statistic.csv****，该文件统计了不同PIPE的总搬运数据量大小、操作数个数以及耗时信息。图1**
Pipe_statistic.csv

关键字段说明如下。**表1**字段说明
字段名

字段解释

Pipe

表示昇腾处理器中不同PIPE单元的名称。

Duration(us)

PIPE耗时，单位us。

Cycle

各个指令每次执行时消耗的cycle数。

Size(B)

表示搬运类PIPE的搬运量大小，单位B。

Ops

表示计算类PIPE的计算元素大小。
|  |  |
| --- | --- |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |

对于流水线耗时最长，明显是搬运性能瓶颈的PIPE，通常有如下优化思路：

- 若搬运数据量较大时，尽可能一次搬运较多的数据，充分利用搬运带宽。
- 尽可能保证性能瓶颈的PIPE在流水上一直在工作。

#### 指令信息统计

**指令信息统计文件Instruction_statistic.csv**，该文件统计了不同指令维度的总搬运数据量大小、操作数个数以及耗时信息，能够发现指令层面上的瓶颈主要在MOV-GM_TO_L1（属于PIPE-MTE2），从指令层面找到了性能瓶颈处。
**图2**
Instruction_statistic.csv关键字段说明如下。**表2**字段说明
字段名

字段解释

Instruction

指令名称。

Duration(us)

PIPE耗时，单位us。

Cycle

各个指令每次执行时消耗的cycle数。

Size(B)

表示搬运类PIPE的搬运量大小，单位B。

Ops

表示计算类PIPE的计算元素大小。
|  |  |
| --- | --- |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
**父主题：**[性能建模](atlasopdev_16_0151.html)