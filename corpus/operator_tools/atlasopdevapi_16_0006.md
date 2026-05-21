---
title: "Tensor.load"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdevapi_16_0006.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdevapi_16_0006.html"
---

# Tensor.load

#### 功能说明

所有的数据搬运指令在msKPP工具下都抽象为load方法，用户只需关心昇腾AI处理器中合理的搬运通路，无需考虑搬运指令中复杂的stride概念。

#### 接口原型

```
1
```

```
Tensor.load(tensor, repeat=1, set_value=-1, expect_value=-1)

```
|  |  |
| --- | --- |

#### 参数说明

参数名

输入类型

说明

tensor

变量

输入的其他tensor，其功能与接口中Tensor的定义一致。

repeat

int

该参数是对搬运指令repeat的模拟，通过输入该值可获取不同repeat值下搬运通路的带宽值，该带宽值用于计算搬运指令的耗时。

非必选参数，默认值为1，建议值为[1,255]之间的整数。

*当输入的repeat值不满足要求时，系统将会抛出异常："input repeat = xx**invalid."，其中xx*为输入的异常repeat值。

set_value

int

设置此tensor数据被依赖的标识号，可以自行定义，需与expect_value配对使用。

非必选参数，不输入则不会使能依赖关系。

expect_value

int

设置此tensor数据加载依赖数据的标识号，可以自行定义，需与set_value配对使用。

非必选参数，不输入则不会使能依赖关系。
|  |  |  |
| --- | --- | --- |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |

#### 约束说明

set_value和expect_value需配对使用，否则可能会造成流水阻塞。

repeat参数仅支持以下4条搬运通路：L1_TO_L0A、L1_TO_L0B、GM_TO_L0A和GM_TO_L0B。
**父主题：**[基础功能接口](atlasopdevapi_16_0002.html)