---
title: "明确优化目标"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_109.html"
date_collected: "2026-05-04"
category: "llm_cases"
original_path: "zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_109.html"
---

# 明确优化目标

用户通常关注首Token时延、吞吐等性能指标。测试时的并发、输入输出长度对性能影响较大，必要时可以进行引导。

- 低时延场景：实时交互（如对话系统），关注首Token生成速度（Prefill阶段优化）。
- 高吞吐场景：离线批量处理（如文档生成），关注Tokens/秒（Decode阶段优化）。
有时性能目标和实际差异较大，可以根据纯模型性能简单评估性能上限，判断时延或吞吐的极限，从而判断目标是否有可能达成。

#### 服务化性能上限评估

按照估算场景和目标划分，基于纯模型测试结果，对于服务化性能上限的几种（乐观）估计方法如下：

- 单并发：与纯模型单并发性能接近。
- 大并发下平均首Token时延。
  - Prefill阶段推理是算力密集型场景，Prefill Batchsize增大后会触发算力瓶颈；触发瓶颈后，Prefill时延会随Batchsize增加接近线性增长。
  - 使用纯模型测试找到达到算力瓶颈的Prefill Batchsize，以这个Prefill Batchsize划分服务化的并发请求数，即基于纯模型结果计算首Token时延上限；假设纯模型测试找到瓶颈处Prefill Batchsize为，此时单个Prefill Batch的纯模型计算时间为，要估计的服务化实际并发为，则服务化此轮并发请求的Prefill总时间估计为，在先来先服务（FCFS）调度策略下，平均首Token时延约为。

- 大并发下吞吐、非首Token时延。
  - Decode是带宽瓶颈而非算力瓶颈，理论单个Decode的Batchsize越大，总吞吐越大，直至达到显存限制。
  - 服务化的输出吞吐和非首Token时延，可参考相同并发（即Decode Batchsize）下的纯模型结果作为理论估计的上限，考虑到服务化推理会有框架侧调度等额外的时间开销，服务化吞吐的乐观估计可折算为纯模型吞吐0.8~0.9倍。

- 显存瓶颈下的最大并发/maxBatchsize的理论上限：Decode阶段maxBatchSize主要受显存限制，可根据KV Cache Block数量和序列长度计算。
  - KV Cache缓存池以Block为单位分配，Block的大小通过MindIE服务化参数配置中的cacheBlockSize设置，一般使用默认值128，即每个Block可存储128个Token，根据使用场景的上下文长度计算每个请求需要占用的KV Cache Block数量：
    - 最大Block数量=Ceil(输入Token数/cacheBlockSize)+Ceil(最大输出Token数/cacheBlockSize)
    - 平均Block数量=Ceil(平均输入Token数/cacheBlockSize)+Ceil(平均输出Token数/cacheBlockSize)。

  - MindIE服务端NPU上KV Cache Block总可用数量 Total Block Num可通过实测获取。
    - 清空/root/mindie/log下的所有旧日志文件，通过使能环境变量MINDIE_LLM_PYTHON_LOG_LEVEL和MINDIE_LLM_PYTHON_LOG_TO_FILE，使MindIE LLM中Python程序运行时产生INFO级别日志并写入文件；
    - 在确定除maxBatchSize之外的其他服务化配置后，使用默认值拉起服务，在服务端拉起成功后，使用grep命令搜索MindIE LLM Python程序日志中的"npuBlockNum"关键字，根据使用的卡数不同会返回多个结果，其中的最小值即为MindIE服务端NPU上KV Cache Block总可用数量，以图1为例，总可用数量为817。**图1**
![](figure/zh-cn_image_0000002535807145.png "点击放大")获取MindIE服务端NPU上KV Cache Block总可用数量示例

  - 为保持最佳性能，maxBatchSize一般不宜超过Floor[Total Block Num/最大Block数量]；若请求之间的上下文长度差距较大，则上限可适当提高至Floor[Total Block Num/平均Block数量]。

**父主题：**[服务化性能调优方法论](toolsample6_108.html)