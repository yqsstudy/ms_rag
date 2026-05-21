---
title: "vshl"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdevapi_16_0058.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdevapi_16_0058.html"
---

# vshl

#### 功能说明

vshl指令抽象。

根据输入类型进行逻辑左移或算术左移。

#### 接口原型

```
1
```

```
class vshl(x, y)

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

输入x向量Tensor。支持UINT16、UINT32、INT16、INT32。

y

输出

Tensor变量

输出y向量Tensor。支持UINT16、UINT32、INT16、INT32。
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
from mskpp import vshl, Tensor
ub_x, ub_z = Tensor("UB"), Tensor("UB")
gm_x = Tensor("GM")
ub_x.load(gm_x)
out = vshl(ub_x, ub_z)()

```
|  |  |
| --- | --- |
**父主题：**[指令接口](atlasopdevapi_16_00071.html)