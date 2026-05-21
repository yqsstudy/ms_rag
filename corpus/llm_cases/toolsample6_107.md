---
title: "纯模型性能调优"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_107.html"
date_collected: "2026-05-04"
category: "llm_cases"
original_path: "zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_107.html"
---

# 纯模型性能调优

常见的模型和使用场景下，如果采用了相同的权重、镜像、部署策略，理论上可以复现相似的性能。

因此出现性能问题后，可以优先对环境变量、涉及性能的开关进行检查，大概率问题在此处（例如没有绑核、内核版本低、日志等级等问题）。

[纯模型性能测试可使用AISBench工具的benchmark-mindie评测插件](https://gitee.com/aisbench/benchmark-mindie/blob/master/README.md#纯模型性能测评)评估。

[如果纯模型测试结果已经出现性能劣化现象，可以进行详细的Profiling性能分析 ，分析方法见模型调优深入分析（MindStudio Insight）](toolsample6_015.html)。

#### 纯模型初步测试

纯模型测试根据用户输入的--batch_size参数确定测试请求的大小，根据--case_pair确定请求输入长度和输出长度的组合，在推理时先处理所有请求的Prefill，再将所有请求组成同一个Decode Batch完成Decode推理。对于基线未覆盖的测试场景，特别是有TTFT或TPOT时延要求的场景，可以参考如下步骤进行纯模型测试。

1. 设置”--case_pair [[输入长度,1]]”, 即可模拟单个Prefill Batch的纯模型测试，此时指定的--batch_size参数记录为prefill_batchsize，测试结果中的”Total Time(s)”记录为prefill_time。
2. 按照实际输入输出长度设置--case_pair参数正常进行测试，此时指定的--batch_size参数记录为decode_batchsize，测试结果中的”Non-first token time(ms)”记录为decode_token_time。
3. 调整decode_batchsize和prefill_batchsize，找到满足要求的配置，如表1所示。
**表1**配置说明
场景

配置方法

不限时延基线吞吐

调大decode_batchsize至OOM。（或选取增速放缓的decode_batchsize）

限制TPOT，不限制TTFT

调整decode_batchsize至decode_token_time刚好满足TPOT限制。

限制TPOT和TTFT

爬坡测试（限制Request Rate）

调整decode_batchsize至decode_token_time刚好满足TPOT限制，调整prefill_batchsize令prefill_time接近TTFT限制。

限制TPOT和TTFT

固定并发（不限制Request Rate）

调整decode_batchsize至decode_token_time刚好满足TPOT限制，设置prefill_batchsize=dp, 调小decode_batchsize直至接近平均TTFT限制。
|  |  |  |
| --- | --- | --- |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |

4. 如需纯模型性能调优（并行策略，环境变量等），对不同的配置重复步骤1直到选取最优配置。
5. 将纯模型的Decode Batchsize和Prefill Batchsize转化为服务化参数maxBatchsize和maxPrefillBatchSize。
6. 设置其他服务化和测试参数，根据实际测试结果调整最大并发Requestrate/maxBatchSize/maxPrefillBatchsize。
**父主题：**[MindIE推理性能解决方案](toolsample6_105.html)