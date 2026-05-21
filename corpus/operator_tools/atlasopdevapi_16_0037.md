---
title: "vcopy"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdevapi_16_0037.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdevapi_16_0037.html"
---

# vcopy

#### 功能说明

vcopy指令抽象

将源地址的Tensor拷贝到目标地址。

#### 接口原型

```
1
```

```
class vcopy(x, y)

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

输入向量Tensor。支持int16、int32、uint16、uint32。

y

输出

Tensor变量

输出向量Tensor。支持int16、int32、uint16、uint32。
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
from mskpp import vcopy, Tensor
ub_x, ub_y = Tensor("UB"), Tensor("UB")
gm_x = Tensor("GM")
ub_x.load(gm_x)
out = vcopy(ub_x, ub_y)()

```
|  |  |
| --- | --- |
**父主题：**[指令接口](atlasopdevapi_16_00071.html)