---
title: "针对目标进行调优"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_110.html"
date_collected: "2026-05-04"
category: "llm_cases"
original_path: "zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_110.html"
---

# 针对目标进行调优

明确优化目标后，再调整服务化参数，从而提升服务化性能。

#### 核心参数介绍

核心参数请参见表1，详细介绍请参见《MindIE LLM开发指南》。
**表1**核心参数说明
**优化方向**

**关键参数**

**推荐值/策略**

**低时延**

maxPrefillBatchSize

小批量（4-16），降低首Token计算量。

supportSelectBatch

false, 强制Prefill优先调度。

maxQueueDelayMicroseconds

≤50ms（减少等待延迟）。

**高吞吐**

maxBatchSize（Decode阶段）

最大化（受显存限制）。

maxPrefillBatchSize/maxPrefillTokens

相对调高，按照实际平均输入折算，使maxPrefilltokens在10000上下。

supportSelectBatch

开启吞吐优先调度。

maxQueueDelayMicroseconds

等待时间加大，让测试开始时尽量组成大的Batch。

RequestRate（通过测试工具设定）

增加下发频率，提高至硬件上限。

Concurrency（通过测试工具设定）

同步逐步提升并发至吞吐饱和点。

序列长度三件套

根据实际场景和要求合理配置maxInputTokenLen，maxIterTimes，maxSeqLen。
|  |  |  |
| --- | --- | --- |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |

#### 手动调优

针对未达成目标的参数进行调优，例如时延不满足目标或吞吐不满足目标。

[调优前可以先确认各个参数的理论上限和理论最优配置，比如计算理论maxBatchSize最优值等，具体计算方法可参考服务化性能上限评估](toolsample6_109.html#ZH-CN_TOPIC_0000002535887093__section11259164975120)。

#### 工具调优

**手动调优需要一定的服务化基础。想要更便捷的调优，可以使用服务化调优工具****（msServiceProfiler**[）的专家建议功能，请参见msserviceprofiler 工具介绍](https://gitee.com/ascend/msit/blob/master/msserviceprofiler/README.md)。 使用专家建议工具需要先使用MindIE Benchmark进行服务化性能测试，专家建议工具会基于MindIE Benchmark测试结果落盘文件给出调优建议。

#### 疑难问题

上边所述的服务化调优，均为黑盒状态下的调优。我们并不清楚请求具体的调度过程，比如哪些请求组成了一个Batch、一个Batch有多大、什么时间执行的Prefill、什么时间执行的Decode等。

**某些问题无法仅靠黑盒调优完成，需要展开进一步分析。与纯模型的性能优化类似，需要借助msServiceProfiler**进行分析。
**父主题：**[服务化性能调优方法论](toolsample6_108.html)