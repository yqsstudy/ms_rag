---
title: "Python接口采集"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/msleaks/atlas_msleaks_0009.html"
date_collected: "2026-05-04"
category: "msleaks"
original_path: "zh/mindstudio/830/T&ITools/msleaks/atlas_msleaks_0009.html"
---

# Python接口采集

msLeaks工具支持通过Python接口自定义设置采集内存范围和采集项，实现精准采集、高效分析。

#### 自定义采集范围

新增Python脚本示例，使用Python脚本自定义采集范围，可支持设置多段采集范围。

示例代码如下：

```
1
2
3
4
5
```

```
import msleaks

msleaks.start()   # 开启采集 
train()           # train()为用户代码
msleaks.stop()    # 退出采集

```
|  |  |
| --- | --- |

#### 自定义设置采集项

支持自定义设置采集项，当前仅支持设置device、level、events和call_stack参数，可根据需求自行设置。

示例代码如下：

```
1
2
3
4
5
6
```

```
import msleaks

msleaks.config(call_stack="c:10,python:5", events="launch,alloc,free", level="0", device="npu")
msleaks.start()   # 开启采集
train()           # train()为用户代码
msleaks.stop()    # 退出采集

```
|  |  |
| --- | --- |
**父主题：**[内存采集](atlas_msleaks_0003.html)