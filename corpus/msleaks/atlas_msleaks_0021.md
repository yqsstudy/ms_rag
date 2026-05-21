---
title: "analyze"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/msleaks/atlas_msleaks_0021.html"
date_collected: "2026-05-04"
category: "msleaks"
original_path: "zh/mindstudio/830/T&ITools/msleaks/atlas_msleaks_0021.html"
---

# analyze

#### 功能说明

msLeaks工具提供的对外分析接口。支持内存泄漏分析和自定义低效内存识别。

- 内存泄漏分析
提供对指定范围内的内存泄漏进行离线分析的功能，支持对msLeaks生成的落盘csv文件进行离线分析，并在检测到指定范围内的内存泄漏时触发告警。当前功能仅适用于HAL内存泄漏分析。

使用该接口前，需要在指定范围内通过mstx的mark进行打点，并使用msLeaks启动用户进程，以获取落盘csv文件。之后，通过该接口输入待分析的csv文件、打点信息以及起始index，即可进行离线泄漏分析。

- 自定义低效内存识别
支持输入自定义参数，对msLeaks生成的落盘csv文件或db文件进行离线低效内存识别。根据自定义参数规范，灵活设置低效内存识别的内存块阈值、关注的低效内存类型，以及临时闲置的API间隔时间，从而精准识别落盘的csv或db文件中的低效内存。

如果输入的csv文件或db文件已有低效内存识别的结果，使用自定义低效内存识别功能时，不会清除原有的低效内存识别结果，而是会在此基础上新增识别结果。如果需要多次执行自定义低效内存识别功能，建议备份原始文件。

#### 函数原型

```
analyze(analyzer_type: str, **kwargs):
```

#### 参数说明

- 内存泄漏分析
[参数为leaks时，请参见check_leaks](atlas_msleaks_0022.html#ZH-CN_TOPIC_0000002538428417)查看参数说明。

- 自定义低效内存识别
[参数为inefficient时，请参见check_inefficient](atlas_msleaks_0023.html#ZH-CN_TOPIC_0000002506468690)查看参数说明。

#### 返回值说明

无返回值。

运行后会输出分析结果。

#### 调用示例

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
```

```
import msleaks
msleaks.analyze("leaks", input_path="user/leaks.csv", mstx_info="test",start_index=0)

msleaks.analyze("inefficient",
		input_path="user/ineff.csv",mem_size=0,
		inefficient_type=["early_allocation","late_deallocation","temporary_idleness"],
		idle_threshold=3000
		)
# input_path以实际路径为准

```
|  |  |
| --- | --- |
**父主题：**[API参考](atlas_msleaks_0017.html)