---
title: "vln"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdevapi_16_0015.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdevapi_16_0015.html"
---

# vln

#### 功能说明

vln指令抽象。

y = vln(x)，x、y按元素取对数。

#### 接口原型

```
1
```

```
class vln(x, y)

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

输入x向量Tensor。支持FP16、FP32。

y

输出

Tensor变量

输出y向量Tensor。支持FP16、FP32。
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
from mskpp import vln, Tensor
ub_x = Tensor("UB")
gm_x = Tensor("GM")
ub_x.load(gm_x)
ub_y = Tensor("UB")
out = vln(ub_x, ub_y)()

```
|  |  |
| --- | --- |
**父主题：**[指令接口](atlasopdevapi_16_00071.html)