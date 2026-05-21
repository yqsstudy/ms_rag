---
title: "vcmpvs_xxx"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdevapi_16_0036.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdevapi_16_0036.html"
---

# *vcmpvs_xxx*

#### 功能说明

vcmpvs_[eq|ge|gt|le|lt|ne]指令抽象，该六条指令性能一致。

vcmpvs_eq: z = (x == y)， x逐元素与y中存储的标量比较相等得到z。

vcmpvs_ge: z = (x >= y)， x逐元素与y中存储的标量比较大于或等于得到z。

vcmpvs_gt: z = (x > y)，x逐元素与y中存储的标量比较大于得到z。

vcmpvs_le: z = (x <= y)， x逐元素与y中存储的标量比较小于或等于得到z。

vcmpvs_lt: z = (x < y)， x逐元素与y中存储的标量比较小于得到z。

vcmpvs_ne: z = (x != y)， x逐元素与y中存储的标量比较不等得到z。

#### 接口原型

```
1
```

```
class vcmpvs(x, y, z)

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

输出向量Tensor。
|  |  |  |  |
| --- | --- | --- | --- |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |

#### 约束说明

Vector指令所有输入输出数据的Tensor均在“UB”空间中，shape需保持一致。

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
from mskpp import vcmpvs, Tensor
ub_x, ub_y, ub_z = Tensor("UB"), Tensor("UB"), Tensor("UB")
gm_x, gm_y = Tensor("GM"), Tensor("GM")
ub_x.load(gm_x)
ub_y.load(gm_y)
out = vcmpvs(ub_x, ub_y, ub_z)()

```
|  |  |
| --- | --- |
**父主题：**[指令接口](atlasopdevapi_16_00071.html)