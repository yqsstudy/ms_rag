---
title: "list_analyzers"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/msleaks/atlas_msleaks_0019.html"
date_collected: "2026-05-04"
category: "msleaks"
original_path: "zh/mindstudio/830/T&ITools/msleaks/atlas_msleaks_0019.html"
---

# list_analyzers

#### 功能说明

该接口可输出msLeaks工具当前支持的所有内存分析类型，且支持用户打印。当前仅支持内存泄漏分析和低效内存识别。

#### 函数原型

```
list_analyzers() -> List[str]
```

#### 参数说明

参数名

输入/输出

说明

List[str]

输出

字符串列表。
|  |  |  |
| --- | --- | --- |
|  |  |  |

#### 返回值说明

无返回值。

运行后会输出当前msLeaks工具支持的内存分析类型。

#### 调用示例

```
1
2
3
```

```
import msleaks
config_list = msleaks.list_analyzers()
print(config_list)

```
|  |  |
| --- | --- |
**父主题：**[API参考](atlas_msleaks_0017.html)