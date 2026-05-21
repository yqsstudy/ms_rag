---
title: "Tensor"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdevapi_16_0005.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdevapi_16_0005.html"
---

# Tensor

#### 功能说明

片上Tensor的抽象，可指定Tensor的内存位置、数据类型、大小及排布格式作为指令的数据依赖标识。

#### 接口原型

```
1
```

```
class Tensor(mem_type, dtype=None, size=None, format=None, is_inited=False)

```
|  |  |
| --- | --- |

#### 参数说明

参数名

输入类型

说明

mem_type

字符串

抽象Tensor所处的内存空间的位置，如“GM”、“UB”、“L1”、“L0A”、“L0B”、“L0C”、“FB”、“BT”等。

dtype

字符串

数据类型，如BOOL、UINT1、UINT2、UINT8、UINT16、UINT32、BF16、UINT64、INT4、INT8、INT16、INT32、INT64、FP16、FP32。

size

list

Tensor的shape。

format

字符串

[数据排布格式，详细可参见《Ascend C算子开发指南](https://www.hiascend.com/document/detail/zh/canncommercial/850/opdevg/Ascendcopdevg/atlas_ascendc_map_10_0002.html)[》中的数据排布格式](https://www.hiascend.com/document/detail/zh/canncommercial/850/opdevg/Ascendcopdevg/atlas_ascendc_10_0099.html)章节。

is_inited

bool

控制Tensor类是否已就绪的开关，开启后，以该Tensor为输入的指令即可启动。
|  |  |  |
| --- | --- | --- |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |

#### 成员

成员名称

描述

tensor.set_valid()

使能当前tensor就绪，开启后，以该tensor为输入的指令即可立即启动。

tensor.set_invalid()

使当前tensor处于非就绪状态，关闭后，以该tensor为输入的指令不可立即启动。

tensor.is_valid()

用于获取当前的tensor就绪状态。
|  |  |
| --- | --- |
|  |  |
|  |  |
|  |  |

#### 约束说明

需通过创建一个shape为[1]且is_inited=True的Tensor进行标量创建。

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
9
```

```
from mskpp import Tensor, Core
gm_tmp= Tensor("GM", "FP16", [48, 16], format="ND")
with Core("AIV0") as aiv:  # AIV0上的相关计算逻辑
    ...
    gm_tmp.load(result, set_value=0)
with Core("AIC0") as aic:
    in_x = Tensor("GM", "FP16", [48, 16], format="ND")
    in_x.load(gm_tmp, expect_value=0) # AIC0上的相关计算逻辑 
    ...

```
|  |  |
| --- | --- |
**父主题：**[基础功能接口](atlasopdevapi_16_0002.html)