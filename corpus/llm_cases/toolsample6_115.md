---
title: "DeepSeek进阶调优"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_115.html"
date_collected: "2026-05-04"
category: "llm_cases"
original_path: "zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_115.html"
---

# DeepSeek进阶调优

进阶调优对于服务化和纯模型都有收益，暂不区分；部分进阶调优手段可能需要相关组件支撑。

#### 显存分析

优化达到瓶颈后，一个直观的方法是优化显存来使用更优的配置（例如并发数，并行策略等），可考虑采用量化来降低计算量和显存，目前适配最好方案为W8A8。

#### 并行策略调优

当前16卡推理场景，一般最优配置是TP=8，DP=2，MOE_TP=4，MOE_EP=4；但用户有不同的Host端（arm/x86），输入输出要求等，这会造成最优的并行策略发生变化，因此需要调整并行策略。

#### 通信策略优化

不同通信策略会产生的通信量不同，需要根据并行策略进行评估。

调优建议：

- Attention的TP尽量减小，增加DP，避免KV Cache复制，避免重复访问和存储。
- 纯DP通信可节省KV Cache，但模型权重需要占更多空间。
- 专家通信（EP）通过ATB-Models安装目录中配置文件config.json里的ep_level关键字配置，AlltoAll理论通信量会少一些。
- 通信可选择走LCCL或者HCCL，通常LCCL性能更优，但部分并行策略下适配可能有问题。

#### 其他优化方法

- 权重格式转换：权重转换为NZ格式，减少格式随路转换耗时。
- 总请求设置：由于Decode阶段性能存在爬坡（受限Request Rate，前期Batch较小，未达到瓶颈，Decode阶段的Batch在逐步提高），因此建议设置总请求数=并发数*10。
**父主题：**[MindIE推理性能解决方案](toolsample6_105.html)