---
title: "msDebug工具在docker中执行"run"命令运行程序后，提示“'A' packet returned an error: 8”"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0132.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0132.html"
---

# msDebug工具在docker中执行"run"命令运行程序后，提示“'A' packet returned an error: 8”

#### 现象描述

在docker中，msDebug工具在执行"run"命令运行程序后，出现以下报错。

```
(msdebug) run
'A' packet returned an error: 8
(msdebug)
...
```

#### 原因分析

出现该错误，可能与“地址空间布局随机化”有关。

#### 解决措施

需输入并执行下列命令来规避此问题。

```
...
(msdebug) settings set target.disable-aslr false
...
```
**父主题：**[FAQ](atlasopdev_16_0077.html)