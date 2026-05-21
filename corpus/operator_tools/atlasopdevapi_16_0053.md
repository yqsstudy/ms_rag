---
title: "vreduce"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdevapi_16_0053.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdevapi_16_0053.html"
---

# vreduce

#### 功能说明

vreduce指令抽象。

vreduce指令根据输入y向量的mask数据，决定取x向量中的某些元素存至z向量，由于msKPP中的Tensor并无实际元素，因此增加了reserve_num的参数，z输出的shape由该参数决定。

#### 接口原型

```
1
```

```
class vreduce(x, y, z, reserve_num)

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

输入x向量Tensor。支持UINT16、UINT32。

y

输入

Tensor变量

输入y向量Tensor。支持UINT16、UINT32。

z

输出

Tensor变量

输出z向量Tensor。支持UINT16、UINT32。

reserve_num

输入

int

指定输出元素的个数。
|  |  |  |  |
| --- | --- | --- | --- |
|  |  |  |  |
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
7
8
```

```
from mskpp import vreduce, Tensor
ub_x, ub_y, ub_z = Tensor("UB"), Tensor("UB"), Tensor("UB")
gm_x, gm_y, gm_z = Tensor("GM"), Tensor("GM"), Tensor("GM")
reserve_num = 16
ub_x.load(gm_x)
ub_y.load(gm_y)
out = vreduce(ub_x, ub_y, ub_z, reserve_num)()
gm_z.load(out[0])

```
|  |  |
| --- | --- |
**父主题：**[指令接口](atlasopdevapi_16_00071.html)