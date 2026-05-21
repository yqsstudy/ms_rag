---
title: "vcpadd"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdevapi_16_0038.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdevapi_16_0038.html"
---

# vcpadd

#### 功能说明

vcpadd指令抽象。

计算输入的x向量的n和n+1的和，n为偶数下标，将结果写回y。reduce_num控制了输出的type。

#### 接口原型

```
1
```

```
class vcpadd(x, y, reduce_num)

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

输入x向量Tensor。支持fp16、fp32。

y

输出

Tensor变量

输出y向量Tensor。支持fp16、fp32。

reduce_num

输入

int

shape指定的缩减倍数。
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
from mskpp import vcpadd, Tensor
ub_x, ub_y = Tensor("UB"), Tensor("UB")
gm_x, gm_y = Tensor("GM"), Tensor("GM")
ub_x.load(gm_x)
ub_y.load(gm_y)
out = vcpadd(ub_x, ub_y, reduce_num)()

```
|  |  |
| --- | --- |
**父主题：**[指令接口](atlasopdevapi_16_00071.html)