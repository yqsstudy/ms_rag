---
title: "vaxpy"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdevapi_16_0027.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdevapi_16_0027.html"
---

# vaxpy

#### 功能说明

vaxpy指令抽象。

z = x * y + z，vaxpy求值向量x与标量y的乘积后加上目标地址z上的和，可以通过if_mix将输出的数据类型格式指定为FP32。

#### 接口原型

```
1
```

```
vaxpy(x, y, z, if_mix=False)

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

输入向量Tensor。支持FP16、FP32、INT16、INT32。

y

输入

Tensor变量

输入标量，程序不对该参数做任何处理。

z

输出

Tensor变量

输出向量Tensor。支持FP16、FP32、INT16、INT32。

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

#### 使用示例

```
1
2
3
4
5
```

```
from mskpp import vaxpy, Tensor
ub_x, ub_z = Tensor("UB"), Tensor("UB")
gm_x = Tensor("GM")
ub_x.load(gm_x)
out = vaxpy(ub_x, ub_y, ub_z)()

```
|  |  |
| --- | --- |
**父主题：**[指令接口](atlasopdevapi_16_00071.html)