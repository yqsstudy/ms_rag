---
title: "简介"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/msleaks/atlas_msleaks_0018.html"
date_collected: "2026-05-04"
category: "msleaks"
original_path: "zh/mindstudio/830/T&ITools/msleaks/atlas_msleaks_0018.html"
---

# 简介

msLeaks工具提供开放接口，帮助用户进行内存分析，识别内存问题。

analyzer类是msLeaks工具新增的离线分析模块，负责所有的离线分析功能。可以从msLeaks导入对应的analyzer分析类，实现内存泄漏分析和自定义低效内存识别。

msLeaks工具提供快速分析接口和analyzer类分析两种方式，进行离线分析。推荐使用快速分析接口。

- 快速分析接口
msLeaks工具提供快速分析接口，推荐直接使用快速分析接口进行离线分析，接口列表如表1所示。
**表1**接口列表
接口

说明

list_analyzers

该接口输出msLeaks工具当前支持的所有内存分析类型。

get_analyzer_config

该接口查看运行相应内存分析类型需要输入的参数。

analyze

msLeaks工具提供的快速分析接口。支持内存泄漏分析和自定义低效内存识别。

check_leaks

msLeaks工具提供的内存泄漏快速分析接口。

check_inefficient

msLeaks工具提供的自定义低效内存识别快速分析接口。
|  |  |
| --- | --- |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |

- analyzer类
可以直接从msLeaks工具导入analyzer类，进行离线分析，涉及的接口如表2所示。但是代码实现较为繁琐，不推荐使用该方式。
实现示例代码如下：
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
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
```

```
# 导入内存泄漏的分析类和对应的config
from msleaks.analyzer import LeaksAnalyzer, LeaksConfig
# 声明参数生成config
leaks_config = LeaksConfig(
    input_path="user/leaks.csv",	# input_path以实际路径为准
    mstx_info="test",
    start_index=0
)
# 生成分析类实例进行分析
leaks_analyzer=LeaksAnalyzer()
leaks_analyzer.analyze(leaks_config)

# 导入低效内存的分析类和对应的config
from msleaks.analyzer import InefficientConfig, InefficientAnalyzer
# 声明参数生成config
ineff_config = InefficientConfig(
    input_path="user/ineff.csv",	# input_path以实际路径为准
    mem_size=0,
    inefficient_type=["early_allocation","late_deallocation","temporary_idleness"],
    idle_threshold=3000
)
# 生成分析类实例进行分析
ineff_analyzer=InefficientAnalyzer()
ineff_analyzer.analyze(ineff_config)

```
|  |  |
| --- | --- |
**表2**analyzer类接口说明
接口

说明

LeaksAnalyzer

内存泄漏分析类。

LeaksConfig

内存泄漏分析参数。

InefficientConfig

低效内存分析参数。

InefficientAnalyzer

低效内存分析类。
|  |  |
| --- | --- |
|  |  |
|  |  |
|  |  |
|  |  |

**父主题：**[API参考](atlas_msleaks_0017.html)