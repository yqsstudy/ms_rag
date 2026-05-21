---
title: "概述"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0307.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0307.html"
---

# 概述

msprof命令行工具是通过msprof.py封装的，用户除了可以直接执行msprof命令行之外，也可通过msprof.py解析性能数据。

- 以下产品不支持在设备上直接解析、查询和导出，需要将采集到的PROF_XXX目录拷贝到安装了CANN-Toolkit开发套件包和ops算子包的环境下进行操作：
  - Atlas 200I/500 A2 推理产品的Ascend RC场景

- 除msprof命令行工具自带解析功能外，其他性能数据采集方式均不支持解析功能，可以选择使用msprof命令行工具或msprof.py工具进行数据解析。
- msprof.py工具使用安装时创建的普通用户运行。
- 未安装驱动和固件的环境仅支持性能数据解析和导出，不支持性能数据采集。
**父主题：**[使用msprof.py脚本解析与导出性能数据](atlasprofiling_16_0306.html)