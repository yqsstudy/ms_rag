---
title: "vcgadd"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdevapi_16_0029.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdevapi_16_0029.html"
---

# vcgadd

#### 功能说明

vcgadd指令抽象

计算每个block元素的和，共计8个block，不支持混合地址。

#### 接口原型

```
1
```

```
class vcgadd(x, y, reduce_num)

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

reduce_num

输入

int

shape指定的缩减倍数。
|  |  |  |  |
| --- | --- | --- | --- |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |

#### 约束说明

reduce_num不能为0。

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
from mskpp import vcgadd, Tensor
ub_x, ub_y = Tensor("UB"), Tensor("UB")
gm_x = Tensor("GM")
reduce_num = 16
ub_x.load(gm_x)
out = vcgadd(ub_x, ub_y, reduce_num)()

```
|  |  |
| --- | --- |
**父主题：**[指令接口](atlasopdevapi_16_00071.html)