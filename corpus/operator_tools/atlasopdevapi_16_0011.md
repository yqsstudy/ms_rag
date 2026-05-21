---
title: "vconv_deq"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdevapi_16_0011.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdevapi_16_0011.html"
---

# vconv_deq

#### 功能说明

vconv_deq指令抽象。

y = vconv_deq(x, dtype)，vconv_deq表示对输入数据进行量化操作的向量计算。

目前支持转换类型包括：FP16->INT8、INT32>FP16。

#### 接口原型

```
1
```

```
class vconv_deq(x, y, dtype)

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

输入x向量Tensor。

y

输出

Tensor变量

输出y向量Tensor。

dtype

输入

字符串

表示目标Tensor的数据类型。
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
from mskpp import vconv_deq, Tensor
ub_x, ub_y = Tensor("UB", "FP16"), Tensor("UB")
gm_x = Tensor("GM")
ub_x.load(gm_x)
out = vconv_deq(ub_x, ub_y, "FP32")()

```
|  |  |
| --- | --- |
**父主题：**[指令接口](atlasopdevapi_16_00071.html)