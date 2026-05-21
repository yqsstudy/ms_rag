---
title: "模型代码优化策略"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_051.html"
date_collected: "2026-05-04"
category: "llm_cases"
original_path: "zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_051.html"
---

# 模型代码优化策略

基于Profiling性能数据， 结合NPU相关的特性， 能够进一步提升模型的性能，具体优化流程请参见图1，常见案例请参见表1。
**图1**
模型代码优化流程
1. 获取模型pr性能数据。
2. 定位到模型性能问题，此处一般是指单点CPU操作或算子执行的耗时过长，超出预期。
3. 基于性能数据中调用栈的关系，找到问题代码段。
4. 深入分析问题代码段，找出具体问题。
5. 采用相应的优化措施，例如通过消除冗余代码或用更亲和的实现方式来替代原有代码，从而提升性能。
**表1**常见微调案例
问题类型

模型问题

代码优化建议

格式转换

基于算子数据，若TransData算子耗时占比较高，具体请参见图2。

尝试禁用自动格式转换。

```
torch.npu.config.allow_internal_format = false
```

变量x1为非连续性转换后的结果，在后续的每次调用都将引入transpose。

```
def forward(self, x):
x=self.fc1(x)
x1=F.relu(x).transpose(1,2)#.contiguous()
x2_1=self.fc2_1(x1)
x2_2=self.fc2_2(x1)
x3=torch.add(x2_1,x2_2)
x4=self.fc3(x3)[:,0,]
returnx4
```

消除调用产生的冗余Transpose，转换后，主动调用连续性转换函数。

```
x1 = F.relu(x).transpose(1, 2).contiguous()
```

冗余代码

变量定义未使用，将会带来额外的内存操作开销。

```
tasks = torch.tensor(tasks).to(self.device)    # 定义后变量不使用
```

消除冗余代码。

小批量多次内存搬运导致大量的memory算子，可通过合并后搬运提升性能。

```
tasks = torch.cat([self.task_tokenizer(x["task"]).to(self.device).unsqueeze(0) for x in batched_inputs], dim=0)
```

在CPU上完成操作后，统一搬运到NPU上运行。

```
tasks = torch.cat([self.task_tokenizer(x["task"]).unsqueeze(0) for x in batched_inputs], dim=0)
tasks=tasks.to(self.device)
```

代码不亲和

算子在极端shape下，性能会发生较大的劣化，以SelectV2算子为例，具体请参见图3。

```
fg_scores_mask = fg_mask[;, ;, None].repeat(1, 1, self.num_classes)
target_scores=torch.where(fg_scores_mask>0,target_scores,0)
```

规避调用此算子，使用矩阵运算替换。

```
fg_scores_mask = fg_mask.unsqueeze(-1)
target_sores*=(fg_scores_mask>0).float()
```
|  |  |  |
| --- | --- | --- |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
**图2**
TransData算子耗时占比高**图3**
**SelectV2算子在极端shape下的性能劣化

父主题：**[算子性能问题优化方案](toolsample6_048.html)