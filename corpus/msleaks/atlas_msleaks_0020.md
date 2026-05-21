---
title: "get_analyzer_config"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/msleaks/atlas_msleaks_0020.html"
date_collected: "2026-05-04"
category: "msleaks"
original_path: "zh/mindstudio/830/T&ITools/msleaks/atlas_msleaks_0020.html"
---

# get_analyzer_config

#### 功能说明

该接口可查看运行对应内存分析类型需要输入的参数。

#### 函数原型

```
get_analyzer_config(analyzer_type: str) -> Dict[str, Any]
```

#### 参数说明

参数名

输入/输出

说明

str

输入

[字符串，代表对应的内存分析类型，可参考list_analyzers](atlas_msleaks_0019.html#ZH-CN_TOPIC_0000002506468688)的输出结果，例如“leaks”或“inefficient”。

Dict[str, Any]

输出

包含所有参数的字典，支持直接打印。
|  |  |  |
| --- | --- | --- |
|  |  |  |
|  |  |  |

#### 返回值说明

无返回值。

运行后会直接输出对应内存分析类型所需的入参信息。

#### 调用示例

```
1
2
3
4
5
```

```
import msleaks
leaks_para = msleaks.get_analyzer_config("leaks")
print(leaks_para)
ineff_para = msleaks.get_analyzer_config("inefficient")
print(ineff_para)

```
|  |  |
| --- | --- |
**父主题：**[API参考](atlas_msleaks_0017.html)