---
title: "vbrcb"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdevapi_16_0009.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdevapi_16_0009.html"
---

# vbrcb

#### 功能说明

vbrcb指令抽象。

根据指令的stride将Tensor进行扩维，由于目前msKPP工具的指令体系里并没有stride的概念，需要用户填写如何扩维倍数，并保持输入输出Tensor的shape维度一致。

#### 接口原型

```
1
```

```
class vbrcb(x, y, broadcast_num)

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

输入x向量Tensor。支持UINT16、UINT32。

y

输出

Tensor变量

输出y向量Tensor。支持UINT16、UINT32。

broadcast_num

输入

int

指定最后一维扩维到多少倍，实测性能数据不同扩维倍数对性能影响不大，因此直接以常用的扩维16倍数据为准（对应指令的dstBlockStride=1，dstRepeatStride=8）。
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
from mskpp import vbrcb, Tensor
ub_x, ub_y = Tensor("UB"), Tensor("UB")
gm_x = Tensor("GM")
broadcast_num = 16
ub_x.load(gm_x)
out = vbrcb(ub_x, ub_y, broadcast_num)()

```
|  |  |
| --- | --- |
**父主题：**[指令接口](atlasopdevapi_16_00071.html)