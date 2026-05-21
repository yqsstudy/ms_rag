---
title: "连接Grafana画图"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0041.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0041.html"
---

# 连接Grafana画图

1. 新建Data sources，如下图：



data source类型选择SQLite类型，如下图：



将解析生成的SQLite数据库文件profiler.db连接到Grafana，并记录datasource uid，如下图：



2. 新建dashboard，导入折线图。

*在/xxx/Ascend/cann-{version}*/tools/msserviceprofiler/python/ms_service_profiler/views/路径下包含可视化文件profiler_visualization.json，修改json文件中datasource的uid为步骤2中记录的uid。

*{version}*为CANN软件包版本，支持CANN 8.1.RC1及之后的版本。



json文件末尾的uid用于唯一标记此dashboard，这里不用修改；title用于给此dashboard命名，默认为Profiler Visualization。



3. 新建dashboard，将修改后的json文件内容粘贴导入，即可在Dashboards中找到相对应名称的dashboard。







**父主题：**[Grafana可视化](atlasprofiling_16_0039.html)