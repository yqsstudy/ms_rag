---
title: "mmad"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdevapi_16_0007.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdevapi_16_0007.html"
---

# mmad

#### 功能说明

完成矩阵乘加操作。

#### 接口原型

```
1
```

```
class mmad(x, y, b, is_inited=False)

```
|  |  |
| --- | --- |

#### 参数说明

参数名

数据类型

说明

x

Tensor变量

左矩阵，在“L0A”空间。支持FP16。

y

Tensor变量

右矩阵，在“L0B”空间。支持FP16。

b

Tensor变量

偏置项，可以在“L0C”空间或Bias Table空间。支持FP32。

is_inited

bool

当输入是在“L0C”空间时，需要加is_inited=True，因为不存在通路将数据从GM直接搬运到L0C。
|  |  |  |
| --- | --- | --- |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |

#### 约束说明

偏置项在Bias Table空间时，其Tensor的数据格式需为ND，shape是[n, ]。

#### 使用示例

```
1
2
3
4
5
```

```
from mskpp import mmad, Tensor
in_x = Tensor("GM", "FP16", [32, 48], format="ND")
in_y = Tensor("GM", "FP16", [48, 16], format="ND")
in_z = Tensor("GM", "FP32", [32, 16], format="NC1HWC0")
out_z = mmad(in_x, in_y, in_z)()

```
|  |  |
| --- | --- |
**父主题：**[指令接口](atlasopdevapi_16_00071.html)