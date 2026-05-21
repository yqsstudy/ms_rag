---
title: "vor"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdevapi_16_0051.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdevapi_16_0051.html"
---

# vor

#### 功能说明

vor指令抽象。

vor指令对输入向量按位取或，每个向量为8*256bits。

#### 接口原型

```
1
```

```
class vor(x, y, z)

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

输入x向量Tensor，支持INT16、 UINT16。

y

输入

Tensor变量

输入y向量Tensor，支持INT16、UINT16。

z

输出

Tensor变量

输出z向量Tensor，支持INT16、UINT16。
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
from mskpp import vor, Tensor
ub_x, ub_y, ub_z = Tensor("UB"), Tensor("UB"), Tensor("UB")
gm_x,gm_y = Tensor("GM"), Tensor("GM")
ub_x.load(gm_x)
ub_y.load(gm_y)
out = vor(ub_x, ub_y, ub_z)()

```
|  |  |
| --- | --- |

#### 约束说明

该指令仅支持普通掩码模式和计数器模式。
**父主题：**[指令接口](atlasopdevapi_16_00071.html)