---
title: "算子设计（msKPP）"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/msquickstart/atlasopdev_16_0003.html"
date_collected: "2026-05-04"
category: "quickstart"
original_path: "zh/mindstudio/830/msquickstart/atlasopdev_16_0003.html"
---

# 算子设计（msKPP）

msKPP工具用于算子开发之前，帮助开发者在秒级时间内获取算子性能建模结果，可快速验证算子的实现方案。

1. [参考环境准备](atlasopdev_16_0004.html#ZH-CN_TOPIC_0000002534510673__section81731814530)，完成msKPP工具相关配置。
2. 使用msKPP接口进行指令级别算子建模，模拟AscendC实现的add算子，示例如下：

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
```

```
# 导入add算子建模需要的msKPP接口
from mskpp import vadd, Tensor, Chip

# 参照add算子在aicore内的指令实现，进行数据搬入->数据计算->数据搬出的过程建模
def my_vadd(gm_x, gm_y, gm_z):
    # 向量Add的基本数据通路:
    #被加数x: GM-UB
    #加数y: GM-UB
    #结果向量z: UB-GM
 
    #定义和分配UB上的变量
    x = Tensor("UB")
    y = Tensor("UB")
    z = Tensor("UB")

    # 将GM上的数据移动到UB对应内存空间上
    x.load(gm_x)
    y.load(gm_y)

    # 当前数据已加载到UB上,调用指令进行计算,结果保存在UB上
    out = vadd(x, y, z)()

    # 将UB上的数据移动到GM变量gm_z的地址空间上 
    gm_z.load(out[0])

if __name__== '__main__':
    with Chip("Ascendxxxyy") as chip:  # xxxyy为用户实际使用的具体芯片类型，可以使用命令npu-smi info进行查询
        chip.enable_trace()
        chip.enable_metrics()

        # 应用算子进行AI Core计算
        in_x = Tensor("GM", "FP16", [32, 48], format="ND") 
        in_y = Tensor("GM", "FP16", [32, 48], format="ND")
        in_z = Tensor("GM", "FP16", [32, 48], format="ND")
        my_vadd(in_x, in_y, in_z)

```
|  |  |
| --- | --- |

[add算子介绍请参见基础矢量算子](https://www.hiascend.com/document/detail/zh/canncommercial/83RC1/opdevg/Ascendcopdevg/atlas_ascendc_10_0033.html)。

3. 通过python3 xxx.py命令执行步骤2[的Python.py脚本，将会在当前目录生成以下结果目录。目录中文件展现的具体内容请参见《算子开发工具用户指南](https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0002.html)[》的“算子设计（msKPP）> 算子计算搬运规格分析](https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0010.html)[、极限性能分析](https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0011.html)[及算子Tiling初步设计](https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0012.html)”章节。

```
1
2
3
4
5
```

```
MSKPP{timestamp}/
├── instruction_cycle_consumption.html
├── Instruction_statistic.csv
├── Pipe_statistic.csv
└── trace.json

```
|  |  |
| --- | --- |
**表1**建模结果文件
文件名称

功能

搬运流水统计（Pipe_statistic.csv）

以PIPE维度统计搬运数据量大小、操作数个数以及耗时信息。

指令信息统计（Instruction_statistic.csv）

统计不同指令维度的总搬运数据量大小、操作数个数以及耗时信息，能够发现指令层面上的瓶颈。

指令占比饼图（instruction_cycle_consumption.html）

以指令维度统计耗时信息，并以饼图形式展示。

指令流水图（trace.json）

以指令维度展示耗时信息，并进行可视化展示。
|  |  |
| --- | --- |
|  |  |
|  |  |
|  |  |
|  |  |

**父主题：**[算子开发工具快速入门](tools_qucikstart_0006.html)