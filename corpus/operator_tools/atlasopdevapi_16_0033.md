---
title: "vcmin"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdevapi_16_0033.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdevapi_16_0033.html"
---

# vcmin

#### 功能说明

vcmin指令抽象。

计算输入的Vector中的元素最小值。

#### 接口原型

```
1
```

```
class vcmin(x, y, reduce_num)

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

输入x向量Tensor，支持FP16、FP32。

y

输出

Tensor变量

输出y向量Tensor，支持FP16、FP32。

reduce_num

输入

int

指定最后一维reduce到多少倍，实测性能数据reduce对性能无影响。
|  |  |  |  |
| --- | --- | --- | --- |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |

#### 约束说明

reduce_num不能为0。

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
from mskpp import vcmin, Tensor
ub_x, ub_y = Tensor("UB"), Tensor("UB")
gm_x = Tensor("GM")
reduce_num = 16
ub_x.load(gm_x)
out = vcmin(ub_x, ub_y, reduce_num)()

```
|  |  |
| --- | --- |
**父主题：**[指令接口](atlasopdevapi_16_00071.html)