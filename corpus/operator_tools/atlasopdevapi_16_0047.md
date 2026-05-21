---
title: "vmla"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdevapi_16_0047.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdevapi_16_0047.html"
---

# vmla

#### 功能说明

vmla指令抽象。

z = x * y + z， x、y按元素相乘，相乘的结果与z按元素相加，可以通过if_mix将输出的数据类型格式指定为FP32。

目前支持：

type = f16，f16 = f16 * f16 + f16。

type = f32，f32 = f32 * f32 + f32。

if_mix = True时，f32 = f16 * f16 + f32。其中x、y向量使用64个元素的f16数据用于计算，源向量仅使用低4个block，4个高block被忽略。Xd是64个元素的包含8个block的f32数据，同时作为目标向量和第三个源向量。

#### 接口原型

```
1
```

```
class vmla(x, y, z, if_mix=False)

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

输入x向量Tensor，支持FP16、FP32。

y

输入

Tensor变量

输入y向量Tensor，支持FP16、FP32。

z

输出

Tensor变量

输出向量Tensor，支持FP16、FP32。

if_mix

输入

Tensor变量

- 默认为False。
- 若设置为True，指定输出数据类型为FP32。
|  |  |  |  |
| --- | --- | --- | --- |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |

#### 约束说明

Vector指令输入输出数据的Tensor均在“UB”空间中。

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
from mskpp import vmla, Tensor
ub_x, ub_y, ub_z = Tensor("UB"), Tensor("UB"), Tensor("UB")
gm_x, gm_y = Tensor("GM"), Tensor("GM")
ub_x.load(gm_x)
ub_y.load(gm_y)
out = vmla(ub_x, ub_y, ub_z)()

```
|  |  |
| --- | --- |
**父主题：**[指令接口](atlasopdevapi_16_00071.html)