---
title: "vlrelu"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdevapi_16_0041.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdevapi_16_0041.html"
---

# vlrelu

#### 功能说明

vlrelu指令抽象。

若x大于等于0，则z=x；若x小于0，则z=x*y，x按元素与标量y相乘。

#### 接口原型

```
1
```

```
class vlrelu(x, y, z)

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

输入y标量。支持float16、float32。

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
from mskpp import vlrelu, Tensor
ub_x, ub_z = Tensor("UB"), Tensor("UB")
gm_x = Tensor("GM")
scalar_y = 5  //5为y标量的值
ub_x.load(gm_x)
out = vlrelu(ub_x, scalar_y, ub_z)()

```
|  |  |
| --- | --- |
**父主题：**[指令接口](atlasopdevapi_16_00071.html)