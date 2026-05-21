---
title: "分析性能数据文件"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_091.html"
date_collected: "2026-05-04"
category: "llm_cases"
original_path: "zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_091.html"
---

# 分析性能数据文件

1. 将收集到的性能数据文件导入至MindStudio Insight工具中进行分析。
2. 分析Free占比，通常情况Atlas 200I A2 加速模块的Free占比应该比较小(<10%)。如图1所示，Free占比超过30%，明显存在异常。需要进一步分析该芯片的OS是否运行了其它业务导致资源占用，进而导致出现等待。
**图1**分析Free占比


3. 分析运行在AI CPU的算子。如图2所示，GridSampler2D运行在AI CPU上。找到问题算子并联系相关责任人，判断该算子是否可以优化为AI Core上运行或进行下一步分析。
**图2**
分析运行在AI CPU的算子

4. 分析运行在AI Core，但是耗时长的算子。如图3所示，Conv2D算子，占据大部分耗时。找到问题算子并联系相关责任人，查看该算子是否可以进行下一步优化。
**图3**
分析运行在AI Core且耗时长的算子

5. op_summary文件分析。

建议以Task Duration降序排序，优先关注耗时较长的算子情况，此类算子为性能瓶颈算子。如果vec_ratio和mac_ratio均没有超过0.8，则说明算子仍有优化空间；如果mtex_ratio较高，则说明数据搬运耗时较高，可考虑与前后算子融合以减少搬运，参数说明如表1所示。
**表1**参数说明
参数

说明

aic_mte1_time(us)

代表MTE1类型指令（L1->L0A/L0B搬运类指令）耗时，不包括搬运等待时间。

aic_mte1_ratio

代表MTE1类型指令（L1->L0A/L0B搬运类指令）的cycle数在total cycle数中的占用比。

aic_mte2_time(us)

代表MTE2类型指令（GM->AICORE搬运类指令）耗时。

aic_mte2_ratio

代表MTE2类型指令（GM->AICORE搬运类指令）的cycle数在total cycle数中的占用比。

aic_mte3_time(us)

代表MTE3类型指令（AICORE->GM搬运类指令）耗时。

aic_mte3_ratio

代表MTE3类型指令（AICORE->GM搬运类指令）的cycle数在total cycle数中的占用比。
|  |  |
| --- | --- |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |

**父主题：**[问题分析](toolsample6_090.html)