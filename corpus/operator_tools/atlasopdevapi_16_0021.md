---
title: "vcadd"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdevapi_16_0021.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdevapi_16_0021.html"
---

# vcadd

#### 功能说明

vcadd指令抽象。

根据指令的入参将Tensor进行reduce维度，在msKPP指令体系里由reduce_num控制shape缩减倍数，并保持输入输出Tensor的shape维度一致。当shape最后一维reduce到1，则将该维度消除。需保证shape中最后一维能够被reduce_num整除且不为0。

#### 接口原型

```
1
```

```
class vcadd(x, y, reduce_num)

```
|  |  |
| --- | --- |

#### 参数说明

参数名

输入/输出

数据类型

说明

x

输入

Tensor变量

输入x向量Tensor。支持FP16、FP32。

reduce_num

输入

int

指定最后一维reduce到多少倍，此参数的取值对该指令的性能无影响。

y

输出

Tensor变量

输出y向量Tensor。支持FP16、FP32。
|  |  |  |  |
| --- | --- | --- | --- |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |

#### 使用示例

```
1
2
3
4
5
6
```

```
from mskpp import vcadd, Tensor
ub_x, ub_y = Tensor("UB"), Tensor("UB")
gm_x = Tensor("GM")
reduce_num = 16
ub_x.load(gm_x)
out = vcadd(ub_x, ub_y, reduce_num)()

```
|  |  |
| --- | --- |

#### 约束说明

reduce_num不能为0。
**父主题：**[指令接口](atlasopdevapi_16_00071.html)