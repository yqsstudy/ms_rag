---
title: "check_leaks"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/msleaks/atlas_msleaks_0022.html"
date_collected: "2026-05-04"
category: "msleaks"
original_path: "zh/mindstudio/830/T&ITools/msleaks/atlas_msleaks_0022.html"
---

# check_leaks

#### 功能说明

msLeaks工具对外提供的内存泄漏快速分析接口。

#### 函数原型

```
check_leaks(input_path: str, mstx_info: str, start_index: int)
```

#### 参数说明

[所有输入的参数需根据list_analyzers](atlas_msleaks_0019.html#ZH-CN_TOPIC_0000002506468688)[和get_analyzer_config](atlas_msleaks_0020.html#ZH-CN_TOPIC_0000002506628526)获取，参数信息请参见表1。
**表1**参数说明
参数名

输入/输出

说明

input_path

输入

使用msLeaks采集的csv文件所在路径，需使用绝对路径。

mstx_info

输入

mark打点使用的mstx文本信息，用于标识泄漏分析的范围。

start_index

输入

开始进行泄漏分析的mstx打点索引。
|  |  |  |
| --- | --- | --- |
|  |  |  |
|  |  |  |
|  |  |  |

#### 返回值说明

无返回值。

运行后会直接打印内存泄漏分析结果。

#### 调用示例

```
1
2
3
```

```
import msleaks
msleaks.check_leaks(input_path="user/leaks.csv",mstx_info="test",start_index=0)
# input_path以实际路径为准

```
|  |  |
| --- | --- |
**父主题：**[API参考](atlas_msleaks_0017.html)