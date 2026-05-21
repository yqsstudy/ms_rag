---
title: "vmaddrelu"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdevapi_16_0043.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdevapi_16_0043.html"
---

# vmaddrelu

#### 功能说明

vmaddrelu指令抽象。

z = RELU(x * z + y)。对两个向量中的每个元素进行乘法和加法，然后对该结果中的每个元素进行MADDRELU操作。

#### 接口原型

```
1
```

```
class vmaddrelu(x, y, z)

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

输入x向量Tensor。支持float16、float32。

y

输入

Tensor变量

输入y向量Tensor。支持float16、float32。

z

输出

Tensor变量

输出向量Tensor。支持float16、float32。
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
from mskpp import vmaddrelu, Tensor
ub_x, ub_y, ub_z = Tensor("UB"), Tensor("UB"), Tensor("UB")
gm_x, gm_y = Tensor("GM"), Tensor("GM")
ub_x.load(gm_x)
ub_y.load(gm_y)
out = vmaddrelu(ub_x, ub_y, ub_z)()

```
|  |  |
| --- | --- |
**父主题：**[指令接口](atlasopdevapi_16_00071.html)