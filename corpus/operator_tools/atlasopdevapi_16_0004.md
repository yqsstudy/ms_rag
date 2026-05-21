---
title: "Core"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdevapi_16_0004.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdevapi_16_0004.html"
---

# Core

#### 功能说明

AI Core抽象，在with语句中实例化并用来明确针对某一AI Core类型进行建模。

#### 接口原型

```
1
```

```
class Core(core_type_name)

```
|  |  |
| --- | --- |

#### 参数说明

参数名

输入类型

说明

core_type_name

string

昇腾计算单元类型字符串，通常可以表示为“AICx”或“AIVx”，其中x为数字，即使用的AI Cube Core/ AI Vector Core的序号。

仅支持A-Za-z0-9中的一个或多个字符。
|  |  |  |
| --- | --- | --- |
|  |  |  |

#### 约束说明

需在with语句下将该类初始化。

#### 使用示例

```
1
2
3
4
```

```
from mskpp import Core
with Core("AIC0") as aic:
    # AI Cube Core 0上的算子计算逻辑相关代码
    ...

```
|  |  |
| --- | --- |
**父主题：**[基础功能接口](atlasopdevapi_16_0002.html)