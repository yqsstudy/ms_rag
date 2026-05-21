---
title: "vnot"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdevapi_16_0050.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdevapi_16_0050.html"
---

# vnot

#### 功能说明

vnot指令抽象。

vnot指令对输入向量按位取反，每个向量为8*256bits。

#### 接口原型

```
1
```

```
class vnot(x, y)

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

输入x向量Tensor，支持INT16、UINT16。

y

输出

Tensor变量

输出y向量Tensor，支持INT16、UINT16。
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
from mskpp import vnot, Tensor
ub_x, ub_y = Tensor("UB"), Tensor("UB")
gm_x = Tensor("GM")
ub_x.load(gm_x)
out = vnot(ub_x, ub_y)()

```
|  |  |
| --- | --- |

#### 约束说明

该指令仅支持普通掩码模式和计数器模式。
**父主题：**[指令接口](atlasopdevapi_16_00071.html)