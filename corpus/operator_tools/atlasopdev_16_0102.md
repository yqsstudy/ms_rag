---
title: "代码指令信息文件"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0102.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0102.html"
---

# 代码指令信息文件

代码指令详细信息文件core*_instr_exe.csv。
**core*.veccore* 或core*.cubecore*目录下存放各计算单元的代码指令详细信息文件，例如core0.veccore0目录下core0.veccore0_instr_exe.csv，“core0”代表核编号，“veccore0”代表子核编号。
 
 图1**
![](figure/zh-cn_image_0000002502586708.png "点击放大")core*_instr_exe.csv文件
 
 
 关键字段说明如下。**表1**字段说明
字段名

字段解释

instr

代码指令名称。

addr

代码指令对应的PC地址。

pipe

PIPE类型，包括指令队列和计算单元。

call_count

该指令的调用次数。

cycles

该指令在AI Vector Core/AI Cube Core上执行的cycle总数。

running_time(us)

指令的有效执行时间，单位us。

detail

指令执行的详细参数。
|  |  |
| --- | --- |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
**父主题：**[msprof op simulator](atlasopdev_16_0130.html)