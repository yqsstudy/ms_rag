---
title: "vsqrt"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdevapi_16_0060.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdevapi_16_0060.html"
---

# vsqrt

#### 功能说明

vsqrt指令抽象。

y = √x， x按元素开平方根。

#### 接口原型

```
1
```

```
class vsqrt(x, y)

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
```

```
from mskpp import vsqrt, Tensor
ub_x, ub_z = Tensor("UB"), Tensor("UB")
gm_x = Tensor("GM")
ub_x.load(gm_x)
out = vsqrt(ub_x, ub_y)()

```
|  |  |
| --- | --- |

#### 约束说明

输入的值应为正数，否则结果未知并产生异常。
**父主题：**[指令接口](atlasopdevapi_16_00071.html)