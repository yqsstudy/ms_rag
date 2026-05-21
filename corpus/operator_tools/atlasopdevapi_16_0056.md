---
title: "vrsqrt"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdevapi_16_0056.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdevapi_16_0056.html"
---

# vrsqrt

#### 功能说明

vrsqrt指令抽象。

浮点数的倒数平方根。

#### 接口原型

```
1
```

```
class vrsqrt(x, y)

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

输出

Tensor变量

输出向量Tensor。支持float16、float32。
|  |  |  |  |
| --- | --- | --- | --- |
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
from mskpp import vrsqrt, Tensor
ub_x, ub_y = Tensor("UB"), Tensor("UB")
gm_x, gm_y = Tensor("GM"), Tensor("GM")
ub_x.load(gm_x)
ub_y.load(gm_y)
out = vrsqrt(ub_x, ub_y)()

```
|  |  |
| --- | --- |

```

```
**父主题：**[指令接口](atlasopdevapi_16_00071.html)