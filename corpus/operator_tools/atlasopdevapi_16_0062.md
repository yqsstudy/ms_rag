---
title: "vsubreluconv"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdevapi_16_0062.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdevapi_16_0062.html"
---

# vsubreluconv

#### 功能说明

vsubreluconv指令抽象。

z = vsubreluconv(x, y)，x、y按元素相减，计算relu值，并对输出做量化操作。

支持的类型转换有FP16->INT8、FP32->FP16、INT16->INT8。

#### 接口原型

```
1
```

```
class vsubreluconv(x, y, z)

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

输入x向量Tensor。支持FP16、FP32、INT16。

y

输入

Tensor变量

输入y向量Tensor。支持FP16、FP32、INT16。

z

输出

Tensor变量

输出向量Tensor。支持FP16、INT8。
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
from mskpp import vsubreluconv, Tensor
ub_x, ub_y, ub_z = Tensor("UB"), Tensor("UB"), Tensor("UB")
gm_x, gm_y = Tensor("GM"), Tensor("GM")
ub_x.load(gm_x)
ub_y.load(gm_y)
out = vsubreluconv(ub_x, ub_y, ub_z)()

```
|  |  |
| --- | --- |
**父主题：**[指令接口](atlasopdevapi_16_00071.html)