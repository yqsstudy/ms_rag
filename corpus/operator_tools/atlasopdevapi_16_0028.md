---
title: "vbitsort"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdevapi_16_0028.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdevapi_16_0028.html"
---

# vbitsort

#### 功能说明

vbitsort指令抽象。

根据x输入进行排序，并在排序后给出元素原始的index数据，因此输出向量Tensor的shape会是x数据的两倍。

#### 接口原型

```
1
```

```
class vbitsort(x, y, z)

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

输入向量Tensor。支持FP16、FP32。

y

输入

Tensor变量

输入向量Tensor。支持UINT32。

z

输出

Tensor变量

输出向量Tensor。支持FP16、FP32。
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
from mskpp import vbitsort, Tensor
ub_x, ub_y, ub_z = Tensor("UB"), Tensor("UB"), Tensor("UB")
gm_x, gm_y = Tensor("GM"), Tensor("GM") 
ub_x.load(gm_x)
ub_y.load(gm_y)
out = vbitsort(ub_x, ub_y, ub_z)()

```
|  |  |
| --- | --- |
**父主题：**[指令接口](atlasopdevapi_16_00071.html)