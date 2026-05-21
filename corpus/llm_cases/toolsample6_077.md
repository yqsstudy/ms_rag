---
title: "前置检查"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_077.html"
date_collected: "2026-05-04"
category: "llm_cases"
original_path: "zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_077.html"
---

# 前置检查

执行深入分析前，需完成以下基础检查：

- **额外进程检查**：排查运行环境中是否存在影响CPU性能的后台进程或插件（通常由业务场景负责人确认，此因素较少成为主因）。
- **任务均衡检查**：通过Profiling工具分析各卡计算耗时。若各卡耗时接近且无明显快慢卡现象，可初步判定任务均衡（业务场景负责人可进一步确认）。如图1所示。**图1**
多卡计算任务相对均衡

- **绑核隔离检查（针对A+K场景）**：在服务器调度能力有限（可能出现CPU核切换或抢占）的A+K场景中，建议尝试绑核隔离任务。
**具体操作：使用taskset**命令，或设置环境变量export CPU_AFFINITY_CONF=1、export CPU_AFFINITY_CONF=2。

[环境变量CPU_AFFINITY_CONF的详细说明请参考《PyTorch 训练模型迁移调优指南](https://www.hiascend.com/document/detail/zh/Pytorch/730/ptmoddevg/trainingmigrguide/PT_LMTMOG_0002.html)[》的“性能调优 > 性能调优方法 > 调度优化 > 绑核优化](https://www.hiascend.com/document/detail/zh/Pytorch/730/ptmoddevg/trainingmigrguide/performance_tuning_0060.html)”章节。

**父主题：**[下发异常分析](toolsample6_075.html)