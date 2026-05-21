---
title: "内存拆解"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/msleaks/atlas_msleaks_0014.html"
date_collected: "2026-05-04"
category: "msleaks"
original_path: "zh/mindstudio/830/T&ITools/msleaks/atlas_msleaks_0014.html"
---

# 内存拆解

msLeaks工具通过增加Python接口，支持用户自行对代码段做描述。

#### 使用方式

在msLeaks工具中，增加Python接口，使用describe标记一个Tensor、一个函数或一段代码，共有3种使用方式。

- 方式一：通过装饰器修饰某个函数，函数内所有内存申请事件的owner属性都会打上标签test1。
```
1
2
3
4
5
```

```
import msleaks.describe as describe

@describe.describer(owner="test1")
def train1():
    pass

```
|  |  |
| --- | --- |

- 方式二：通过with语句，对代码块做标记，代码块内所有内存申请事件的owner属性都会打上标签test2。代码示例1：
```
1
2
3
4
```

```
import msleaks.describe as describe

with describe.describer(owner="test2"):
    train2()

```
|  |  |
| --- | --- |
代码示例2：
```
1
2
3
4
5
```

```
import msleaks.describe as describe

describe.describer(owner="test3").__enter__()
train3()
describe.describer(owner="test3").__exit__()

```
|  |  |
| --- | --- |

方式一和方式二最多支持添加3个标签，且不允许重复。

- 方式三：标记Tensor，该Tensor对应的内存申请事件的owner属性会增加用户指定的标记。
```
1
2
3
4
```

```
import msleaks.describe as describe

t = torch.randn(10,10).to('npu:0')
describe.describer(t, owner="test4")

```
|  |  |
| --- | --- |

#### 结果说明

[内存拆解的输出文件详解可参见输出说明](atlas_msleaks_0016.html#ZH-CN_TOPIC_0000002506628524)。
**父主题：**[内存分析](atlas_msleaks_0004.html)