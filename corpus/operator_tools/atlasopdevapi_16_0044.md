---
title: "vmaxs"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdevapi_16_0044.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdevapi_16_0044.html"
---

# vmaxs

#### 功能说明

vmaxs指令抽象。

对向量中的每个元素和标量进行比较，返回较大者。

#### 接口原型

```
1
```

```
class vmaxs(x, y, z)

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

输入x向量Tensor。支持float16、float32、int16、int32。

y

输入

Tensor变量

输入标量。程序不对该参数做任何处理。

z

输出

Tensor变量

输出向量Tensor。支持float16、float32、int16、int32。
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
from mskpp import vmaxs, Tensor
ub_x, ub_z = Tensor("UB"), Tensor("UB")
gm_x = Tensor("GM")
ub_x.load(gm_x)
out = vmaxs(ub_x, 5, ub_z)()

```
|  |  |
| --- | --- |
**父主题：**[指令接口](atlasopdevapi_16_00071.html)