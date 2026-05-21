---
title: "快速排查"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_007.html"
date_collected: "2026-05-04"
category: "llm_cases"
original_path: "zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_007.html"
---

# 快速排查

快速排查分为开箱和长稳两种场景，具体介绍如下：

1. 开箱场景：开箱性能问题场景一般指首次加载模型。此时需要明确性能优化目标，如果存在竞品性能参考，则可以通过Profiling等工具详细对比二者差异。建议在正式拉起任务前，先考虑并行策略寻优，确认最优并行策略。若无法解决问题，参考长稳场景定位方案。
2. 长稳场景：长期稳定性下的性能问题通常指的是系统在一段时间内表现良好且没有性能问题的情况下，突然出现性能下降或性能问题。
  1. [变更排查：明确近期是否进行过变更，包括但不限于集群重新规划、版本变更等。若性能问题在变更后出现，条件允许的情况下，可以尝试撤销近期变更，若确认问题由变更引起，建议优先考虑版本问题或变更涉及操作（如重启）等对集群可能的影响，具体请参见版本升级性能劣化定位方法论](toolsample6_116.html)。
  2. [硬件排查：当性能出现波动时，应检查相应时间点是否有硬件问题，例如NPU降频、网络丢包等硬件告警。注意，这里的硬件排查仅指初步排查，主要关注硬件告警。若无硬件告警或如网络丢包等关键事件，则参考详细排查](toolsample6_008.html)进行定位

**父主题：**[排查思路介绍](toolsample6_006.html)