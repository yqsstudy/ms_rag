---
title: "vtranspose"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdevapi_16_0063.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdevapi_16_0063.html"
---

# vtranspose

#### 功能说明

vtranspose指令抽象。

从输入地址x（32字节对齐）开始转置一个16x16矩阵，每个元素为16位，结果输出到y中，输入输出都是连续的512B存储空间。

#### 接口原型

```
1
```

```
class vtranspose (x, y)

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

输入x向量Tensor。支持INT16。

y

输出

Tensor变量

输出向量Tensor。支持INT16。
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
from mskpp import vtranspose, Tensor
ub_x, ub_y = Tensor("UB"), Tensor("UB")
gm_x = Tensor("GM")
ub_x.load(gm_x)
out = vtranspose(ub_x, ub_y)()

```
|  |  |
| --- | --- |
**父主题：**[指令接口](atlasopdevapi_16_00071.html)