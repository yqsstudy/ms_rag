---
title: "算子性能问题定位方法"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_049.html"
date_collected: "2026-05-04"
category: "llm_cases"
original_path: "zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_049.html"
---

# 算子性能问题定位方法

算子性能问题是深度学习模型中的一个关键挑战，具体表现为部分基础计算单元的执行效率低下，从而影响整个模型的运行速度并造成资源浪费。这类问题需要借助专门的分析工具和代码优化技术来解决。例如，在评估融合算子性能时，可以通过对比不同配置下的计算时间、内存使用量等指标来进行综合判断。
**图1**
算子性能问题定位**表1**算子性能问题定位方法
分析方式

分析目的

处理思路

advisor分析

AI CPU算子耗时占比问题。

降低AI CPU算子耗时。

AI CPU算子首先基于算子名在时间线（Timeline）中定位算子位置，接着基于调用栈找到代码中的位置，然后尝试相同逻辑替换，如果无法替换，可记录算子shape、type等信息并联系算子负责人，确认是否支持该case。

算子编译问题
可尝试在Python训练开始前添加如下代码，指定二进制模式。如果无效则记录算子shape、type等信息并联系算子负责人，确认是否支持该case。
```
torch_npu.npu.set_compile_mode(jit_compile=False)  torch_npu.npu.config.allow_internal_format = False
```

单算子分析

vector算子分析

- vector算子优化方法是通过修改代码逻辑进行消减，优化逻辑如下：
  - [算子亲和优化：具体请参见亲和算子优化策略](toolsample6_050.html)。
  - [模型代码优化：结合算子分析， 模型代码层面尝试对算子调用，如冗余消除、shape优化、等效替换等修改， 具体请参见模型代码优化策略](toolsample6_051.html)。
  - 版本更新：联系昇腾社区反馈，确认新版本是否有优化或后续优化的计划。

- 根据advisor可融合算子分析，排查是否有设计融合算子的必要。若有必要，开发者也可尝试自行开发融合算子进行替换。

cube算子分析

[基于模型调优深入分析（MindStudio Insight）](toolsample6_015.html)中的operator页签，查看算子占比，选取最高耗时的TopN算子，并详细分析input shape下平均aicore性能，记录异常算子及shape，并联系算子负责人确认优化计划。

- MAC ratio：表示cube计算单元是否充分使用，一般理想情况是80%。
- MTE ratio：算子中内存搬运过程，若MTE ratio值过高，则表示内存搬运存在瓶颈。

当算子性能无法达成预期， 优化步骤如下：

- [算子亲和优化：具体请参见亲和算子优化策略](toolsample6_050.html)。
- [模型代码优化：结合算子分析， 模型代码层面尝试对算子调用，如冗余消除、shape优化、等效替换等修改，具体请参见模型代码优化策略](toolsample6_051.html)。
- 版本更新：联系昇腾社区反馈，确认新版本是否有优化或后续优化的计划。

融合算子/亲和API替换

使用融合算子/亲和API替换，可减少不必要的小算子下发，提高AI Core利用率。

advisor中Affinity API Issues分析器可自动识别融合算子，结合调用栈可定位代码位置，进行融合算子/亲和API替换。

融合算子开发

如需进一步提升模型性能，可以考虑进行融合算子开发，融合算子主要为了减少小算子下发，进而减少空闲时间占比。

advisor csv交付件中，针对Host瓶颈和MTE瓶颈的算子序列分析结果已充分展现，并清晰标注了算子序列存在Host瓶颈或MTE瓶颈。为了进一步提升性能，建议深入剖析代码逻辑，判断能否通过算子合并等手段缓解瓶颈现象。
|  |  |  |
| --- | --- | --- |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
**父主题：**[算子性能问题优化方案](toolsample6_048.html)