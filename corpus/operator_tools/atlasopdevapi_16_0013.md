---
title: "vector_dup"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdevapi_16_0013.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdevapi_16_0013.html"
---

# vector_dup

#### 功能说明

vector_dup指令抽象。

y = vector_dup(x)， x、 y按元素进行填充。

#### 接口原型

```
1
```

```
class vector_dup(x, y, fill_shape)

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

输入x向量Tensor。支持FP16、FP32、INT16、INT32、UINT16、UINT32。

y

输出

Tensor变量

输出y向量Tensor。支持FP16、FP32、INT16、INT32、UINT16、UINT32。

fill_shape

输入

list

表示目标Tensor的要被扩充的shape值。
|  |  |  |  |
| --- | --- | --- | --- |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |

#### 约束说明

由于该指令输入仅一个标量，因此需要创建一个shape为[1]且is_inited=True的Tensor作为模拟标量输入，不增加性能开销。

#### 使用示例

```
from mskpp import vector_dup, Tensor
ub_x = Tensor("UB", "FP16", [1], format="ND", is_inited=True)
ub_y = Tensor("UB")
out = vector_dup(ub_x, ub_y, [8, 2048])()
```
**父主题：**[指令接口](atlasopdevapi_16_00071.html)