---
title: "vcgmin"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdevapi_16_0031.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdevapi_16_0031.html"
---

# vcgmin

#### 功能说明

vcgmin指令抽象

计算每个block的最小元素，共计8个block，不支持混合地址。

#### 接口原型

```
1
```

```
class vcgmin(x, y, reduce_num)

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

输入x向量Tensor，支持FP16。

y

输出

Tensor变量

输出y向量Tensor，支持FP16。

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
from mskpp import vcgmin, Tensor
ub_x, ub_y = Tensor("UB"), Tensor("UB")
gm_x = Tensor("GM")
reduce_num = 16
ub_x.load(gm_x)
out = vcgmin(ub_x, ub_y, reduce_num)()

```
|  |  |
| --- | --- |
**父主题：**[指令接口](atlasopdevapi_16_00071.html)