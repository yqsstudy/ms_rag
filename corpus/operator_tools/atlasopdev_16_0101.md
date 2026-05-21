---
title: "代码行耗时数据文件"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0101.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0101.html"
---

# 代码行耗时数据文件

代码行耗时数据文件core*_code_exe.csv。
**core*.veccore* 或core*.cubecore*目录下存放各计算单元的代码行耗时文件，例如core0.veccore1目录下的core0.veccore1_code_exe.csv文件，“core0”代表核编号，“veccore1”代表子核编号。图1**
core*_code_exe.csv文件关键字段说明如下。**表1**字段说明
字段名

字段解释

code

代码行，格式为代码文件路径:行号。

call_count

对应代码行所涉及指令的调用次数。

cycles

该代码行所涉及的指令在AI Vector Core/AI Cube Core上执行的cycle总数。

running_time(us)

代码行的有效执行时间，单位us。
|  |  |
| --- | --- |
|  |  |
|  |  |
|  |  |
|  |  |
**父主题：**[msprof op simulator](atlasopdev_16_0130.html)