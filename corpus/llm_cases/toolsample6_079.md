---
title: "CPU运行状态"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_079.html"
date_collected: "2026-05-04"
category: "llm_cases"
original_path: "zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_079.html"
---

# CPU运行状态

[完成前置检查](toolsample6_077.html)后，执行以下步骤检查CPU状态：

- **命令输入：在命令行执行top****命令，实时查看系统CPU运行状态。图1**
top命令执行界面
- **进程线程查看****： 如需查看特定进程（PID）的所有线程，执行：top -H -p <pid>。图2**
top查看指定进程
- **界面操作说明**：
  - F键：进入字段选择模式
  - 方向键↑/↓：浏览字段
  - D键：选定/取消显示项
  - 方向键→：选中字段，通过方向键与其他字段交换排序位置
  - 方向键←：退出排序操作
**图3**
top界面选择展示参数
- **结果分析与处理**：
  - 按F键并添加P（Last used CPU）字段后，可观察各进程最后运行的CPU核编号。
  - 若发现进程CPU核存在异常切换，可能原因包括：虚拟机或容器内CPU拓扑结构差异，或绑核范围过大。
  - 针对后者，可设置export CPU_AFFINITY_CONF=2，尝试细粒度的绑核优化。
**图4**
显示各进程最后使用CPU
**父主题：**[正式分析](toolsample6_078.html)