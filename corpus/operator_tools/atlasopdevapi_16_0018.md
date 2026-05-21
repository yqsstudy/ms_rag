---
title: "vmuls"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdevapi_16_0018.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdevapi_16_0018.html"
---

# vmuls

#### 功能说明

vmuls指令抽象。

z = vmuls(x, y)，vmuls求值向量x与标量y的乘积。

#### 接口原型

```
1
```

```
class vmuls(x, y, z)

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

Python标量

输入标量，程序不对该参数做任何处理。

z

输出

Tensor变量

输出向量Tensor。支持FP16、FP32、INT16、INT32。
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
```

```
from mskpp import vmuls, Tensor
ub_x, ub_z = Tensor("UB"), Tensor("UB")
gm_x = Tensor("GM")
ub_x.load(gm_x)
out = vmuls(ub_x, 5, ub_z)()  //5为y标量的值

```
|  |  |
| --- | --- |
**父主题：**[指令接口](atlasopdevapi_16_00071.html)