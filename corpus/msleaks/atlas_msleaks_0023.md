---
title: "check_inefficient"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/msleaks/atlas_msleaks_0023.html"
date_collected: "2026-05-04"
category: "msleaks"
original_path: "zh/mindstudio/830/T&ITools/msleaks/atlas_msleaks_0023.html"
---

# check_inefficient

#### 功能说明

msLeaks工具对外提供的自定义低效内存识别快速分析接口。

#### 函数原型

```
check_inefficient(input_path: str, mem_size: int = 0, inefficient_type: List[str] = None, idle_threshold: int = 3000)    # 如果无输入采用默认值
```

#### 参数说明

[所有输入的参数需根据list_analyzers](atlas_msleaks_0019.html#ZH-CN_TOPIC_0000002506468688)[和get_analyzer_config](atlas_msleaks_0020.html#ZH-CN_TOPIC_0000002506628526)获取，参数信息请参见表1。
**表1**参数说明
参数名

输入/输出

说明

input_path

输入

需要进行离线自定义低效内存识别处理的csv或者db文件路径。

mem_size

输入

低效内存阈值，单位：Bytes，低于该阈值的显存块不会输出结果。

inefficient_type

输入

低效类型分类，确定判断策略，仅输出用户关注的低效内存类型。当前支持的类型如下：

- 过早申请：early_allocation
- 过迟释放：late_deallocation
- 临时闲置：temporary_idleness

idle_threshold

输入

临时闲置阈值，决定临时闲置低效内存API阈值，可以灵活设置阈值大小。
|  |  |  |
| --- | --- | --- |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |

#### 返回值说明

无返回值。

运行后会打印提示分析过程，并识别结果写到原文件中。

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
msleaks.check_inefficient(input_path="user/ineff.csv",mem_size=0,
			  inefficient_type=["early_allocation","late_deallocation","temporary_idleness"],idle_threshold=3000
			  )
# input_path以实际路径为准

```
|  |  |
| --- | --- |
**父主题：**[API参考](atlas_msleaks_0017.html)