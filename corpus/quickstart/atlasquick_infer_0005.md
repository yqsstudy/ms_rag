---
title: "性能调优"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/msquickstart/atlasquick_infer_0005.html"
date_collected: "2026-05-04"
category: "quickstart"
original_path: "zh/mindstudio/830/msquickstart/atlasquick_infer_0005.html"
---

# 性能调优

#### 前提条件

[在使用性能调优工具前，请先阅读《性能调优工具用户指南](https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0001.html)[》中的“使用前准备](https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0002.html)”章节的使用约束，了解相关约束条件。

#### 性能数据采集

msprof命令行工具提供了AI任务运行性能数据、昇腾AI处理器系统数据等性能数据的采集和解析能力。

1. 登录Ascend-cann-toolkit开发套件包所在环境，进入“${install_path}/cann/tools/profiler/bin”。${install_path}为CANN Toolkit开发套件包和ops算子包的安装路径。
2. 执行以下命令，采集性能数据。此处对浮点模型进行性能数据采集。
********
```
msprof --output=${output_dir} bash ${ATB_SPEED_HOME_PATH}/examples/models/llama3/run_pa.sh --model_path ${model_path} ${max_output_length}
```

其中--output为采集到的性能数据的存放路径；max_output_length为对话测试中最大输出token数。

3. 命令执行后，回显中包含如下内容，表示采集完成。

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
```

```
[INFO] Start export data in PROF_000001_20241118061102981_MORBFBJDEPNJEQPA.
[INFO] Export all data in PROF_000001_20241118061102981_MORBFBJDEPNJEQPA done.
[INFO] Start query data in PROF_000001_20241118061102981_MORBFBJDEPNJEQPA.
Job Info	Device ID	Dir Name	Collection Time           	Model ID	Iteration Number	Top Time Iteration	Rank ID	

NA      		        host    	2024-11-18 06:11:02.985433	N/A     	N/A             	N/A               	1      	

NA      	1        	device_1	2024-11-18 06:11:07.222675	N/A     	N/A             	N/A               	1 

[INFO] Query all data in PROF_000001_20241118061102981_MORBFBJDEPNJEQPA done.   
[INFO] Profiling finished.
[INFO] Process profiling data complete. Data is saved in {output_dir}/PROF_000001_20241118061102981_MORBFBJDEPNJEQPA

```
|  |  |
| --- | --- |

4. 采集完成后，在--output指定的目录下生成了PROF_000001_20241118061102981_MORBFBJDEPNJEQPA目录，存放采集到的性能数据。
PROF_000001_20241118061102981_MORBFBJDEPNJEQPA目录下的mindstudio_profiler_output目录，存放的是解析后的性能数据，文件结构如下。**
```
├── host   # 保存原始数据，用户无需关注
│    └── data
├── device_{id}   # 保存原始数据，用户无需关注
│    └── data
├── mindstudio_profiler_log   # 采集日志
│    └── log
└── mindstudio_profiler_output
      ├── msprof_20241118061314.json        # timeline数据总表
      ├── op_summary_20241118061317.csv     # AI Core和AI CPU算子数据
      ├── task_time_20241118061317.csv      # Task Scheduler任务调度信息
      ├── op_statistic_20241118061317.csv   # AI Core和AI CPU算子调用次数及耗时统计
      ├── api_statistic_20241118061317.csv  # CANN层的API执行耗时信息统计
      └── README.txt
```

#### 性能数据分析

为了方便分析采集到的性能数据，可使用MindStudio Insight工具将性能数据可视化展示，便于直观地分析性能瓶颈。

1. 打开MindStudio Insight工具。
2. 将4采集到的性能数据拷贝至本地。
3. 单击MindStudio Insight界面左上方“导入数据”，在弹框中选择性能数据文件或目录，然后单击“确认”进行导入，如图1所示。
**图1**
导入数据

4. 根据MindStudio Insight工具的可视化呈现性能数据，如图2所示。
**图2**
展示性能数据

5. 分析性能数据。

[MindStudio Insight工具将性能数据可视化呈现后，可以更直观地分析性能瓶颈，详细分析方法请参见《MindStudio Insight工具用户指南](https://www.hiascend.com/document/detail/zh/mindstudio/830/GUI_baseddevelopmenttool/msascendinsightug/Insight_userguide_0002.html)》。

**父主题：**[模型推理](atlasquick_infer_0002.html)