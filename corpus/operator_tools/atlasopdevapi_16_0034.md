---
title: "vcmp_xxx"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdevapi_16_0034.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdevapi_16_0034.html"
---

# *vcmp_xxx*

#### 功能说明

vcmp_[eq|ge|gt|le|lt|ne]指令抽象，该六条指令性能一致。

vcmp_eq: z = (x == y)， x、y按元素比较相等得到z。

vcmp_ge: z = (x >= y)， x、y按元素比较大于或等于得到z。

vcmp_gt: z = (x > y)， x、y按元素比较大于得到z。

vcmp_le: z = (x <= y)， x、y按元素比较小于或等于得到z。

vcmp_lt: z = (x < y)， x、y按元素比较小于得到z。

vcmp_ne: z = (x != y)， x、y按元素比较不等得到z。

#### 接口原型

```
1
```

```
class vcmp(x, y)

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

输出

Tensor变量

输出y向量Tensor，支持FP16、FP32。
|  |  |  |  |
| --- | --- | --- | --- |
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
from mskpp import vcmp, Tensor
ub_x, ub_y = Tensor("UB"), Tensor("UB")
gm_x, gm_y = Tensor("GM"), Tensor("GM")
ub_x.load(gm_x)
ub_y.load(gm_y)
out = vcmp(ub_x, ub_y)()

```
|  |  |
| --- | --- |
**父主题：**[指令接口](atlasopdevapi_16_00071.html)