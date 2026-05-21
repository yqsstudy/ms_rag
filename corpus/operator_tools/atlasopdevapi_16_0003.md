---
title: "Chip"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdevapi_16_0003.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdevapi_16_0003.html"
---

# Chip

#### 功能说明

处理器抽象，在with语句中实例化并用来明确针对某一昇腾AI处理器类型进行建模。

#### 接口原型

```
1
```

```
class Chip(name, debug_mode=False)

```
|  |  |
| --- | --- |

#### 参数说明

参数名

输入类型

说明

name

string

处理器名称。

**目前大部分数据基于Atlas A2 训练系列产品/Atlas A2 推理系列产品采集，使用npu-smi info**可以查看当前设备昇腾AI处理器类型。

debug_mode

bool

是否启用调试模式，默认为False。

- True：启用
- False：不启用
说明：
开启debug模式后可查看未正确运行的指令，但不会生成任何输出件。
|  |  |  |
| --- | --- | --- |
|  |  |  |
|  |  |  |

#### 成员

成员名称

描述

chip.enable_trace()

使能算子模拟流水图的功能，生成流水图文件trace.json。

chip.enable_metrics()

使能单指令及分PIPE的流水信息，生成指令统计（Instruction_statistic.csv）、搬运流水统计（Pipe_statistic.csv）文件和指令占比饼图（instruction_cycle_consumption.html）。

chip.set_cache_hit_ratio(config)

[用于使能手动调整L2Cache命中率，其中config = {"cache_hit_ratio": 0.6}，具体介绍请参见支持cache命中率建模章节](https://www.hiascend.com/document/detail/zh/mindstudio/82RC1/ODtools/Operatordevelopmenttools/atlasopdev_16_0009.html)。

chip.set_prof_summary_path("xxx/PipeUtilization.csv")

[其中PipeUtilization.csv为msprof的结果示例，用于使能PIPE信息的理论值与msprof实测值比对。具体介绍请参见支持PIPE信息的理论值与msprof实测值比对章节](https://www.hiascend.com/document/detail/zh/mindstudio/82RC1/ODtools/Operatordevelopmenttools/atlasopdev_16_0009.html)。

chip.disable_instr_log()

使能后，抑制指令任务添加和调度结束后的日志打印。
|  |  |
| --- | --- |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |

#### 约束说明

需在with语句下将该类初始化。

#### 使用示例

```
1
2
3
4
5
```

```
from mskpp import Chip
# 如何查看当前设备昇腾处理器类型请参见以下说明
with Chip("Ascendxxxyy") as chip:    # Ascendxxxyy需替换为实际使用的处理器类型
    chip.enable_trace()   # 调用该函数即可使能算子模拟流水图的功能，生成流水图文件
    chip.enable_metrics()  # 调用该函数即可使能单指令及分PIPE的流水信息，生成搬运流水统计、指令信息统计和指令占比饼图

```
|  |  |
| --- | --- |

**非Atlas A3 训练系列产品/Atlas A3 推理系列产品：在安装昇腾AI处理器的服务器执行npu-smi info****命令进行查询，获取Chip Name****信息。实际配置值为AscendChip Name，例如Chip Name***取值为xxxyy**，实际配置值为Ascendxxxyy**。当Ascendxxxyy为代码样例的路径时，需要配置为ascendxxxyy*。
**父主题：**[基础功能接口](atlasopdevapi_16_0002.html)