---
title: "配合mstx接口实现范围级重放"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0187.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0187.html"
---

# 配合mstx接口实现范围级重放

展示如何使用msProf工具配合mstx接口实现范围级重放，以保留算子执行时上下文的L2Cache信息。

#### 前提条件

[准备算子工程，并在算子代码中添加mstx扩展接口确定范围级重放的范围，具体请参见mstx扩展功能](atlasopdev_16_0115.html#ZH-CN_TOPIC_0000002505040660)[和 《MindStudio mstx API参考](https://www.hiascend.com/document/detail/zh/mindstudio/830/API/mstxAPIReference/msprof_tx_0001.html)》。

- 
mstxRangeStartA和mstxRangeEnd接口需成对调用，不支持交叉调用。每一对mstx API中包含的算子为一个重放范围，该重放范围内算子的Stream不能改变。

- [每一个重放范围能采集的算子数量受OpBasicInfo（算子基础信息）](atlasopdev_16_0098.html#ZH-CN_TOPIC_0000002505040646)中算子Block Dim数量限制，建议不超过50个。
- 使用该功能时，不支持与--aic-metrics=MemoryDetail、--aic-metrics=TimelineDetail及--aic-metrics=Source同时使能；不建议与--kill=on同时使能，否则可能导致采集的算子数据缺失。
- 在进行范围级重放时，执行算子SynchronizeStream可能会失败，建议在mstxRangeEnd接口调用结束后再执行。
- 该功能仅适用于Atlas A3 训练系列产品/Atlas A3 推理系列产品和Atlas A2 训练系列产品/Atlas A2 推理系列产品。

#### 调用示例

以Python API接口方式（test.py文件）为例，说明msProf工具如何配合mstx接口实现范围级重放。

```
import mstx
import torch
import torch_npu
 
x = torch.Tensor([1,2,3,4]).npu()
y = torch.Tensor([1,2,3,4]).npu()

a = x + y
range1_id = mstx.range_start("range1", None)
b = a - x
c = a * x
mstx.range_end(range1_id)
range2_id = mstx.range_start("range2", None)
d = x / y
range3_id = mstx.range_start("range3", None)
e = torch.abs(y)
mstx.range_end(range3_id)
f = x + e
mstx.range_end(range2_id)
```

#### 操作步骤
单range范围级重放
1. 执行以下命令，使能单一mstx API范围，以下命令将执行“range1”范围级重放。
```
msprof op --replay-mode=range --mstx=on --mstx-include="range1" --launch-count=10 python3 test.py
```

2. [工具生成Sub、Mul算子的调优数据，且两个算子之间的L2Cache信息会保留。具体性能文件介绍请参考表2](atlasopdev_16_00851.html#ZH-CN_TOPIC_0000002536920559__zh-cn_topic_0000002534426389_table056510168348)。**********
```
OPPROF_{timestamp}_XXX
├── Mul_XXX  // Mul_XXX为采集算子名称
│   └── 0
│       ├── dump
                ...
│       └── visualize_data.bin
└── Sub_XXX
    └── 0
        ├── dump
               ...
        └── visualize_data.bin
```

- 多range范围级重放
  1. 执行以下命令，使能所有mstx API范围。
```
msprof op --replay-mode=range --mstx=on --launch-count=10 python3 test.py
```

  2. [工具将会先后执行“range1”和“range2”范围级重放，生成Sub、Mul、Div、Abs、Add算子的调优数据，每次重放算子之间的L2Cache信息会保留，但两次重放的L2Cache信息互相独立。但因为“range2”和“range3”存在范围交叉，则仅第一个范围生效，“range3”将无效。具体性能文件介绍请参考表2](atlasopdev_16_00851.html#ZH-CN_TOPIC_0000002536920559__zh-cn_topic_0000002534426389_table056510168348)。****************
```
OPPROF_{timestamp}_XXX
├── Abs_XXX  // Abs_XXX为采集算子名称
│   └── 0
│       ├── dump
                ...
│       └── visualize_data.bin
├── Add_XXX
│   └── 0
│       ├── dump
                ...
│       └── visualize_data.bin
├── Mul_XXX
│   └── 0
│       ├── dump
                ...
│       └── visualize_data.bin
├── RealDiv_XXX
│   └── 0
│       ├── dump
                ...
│       └── visualize_data.bin
└── Sub_XXX
    └── 0
        ├── dump
               ...
        └── visualize_data.bin
```

**父主题：**[典型案例](atlasopdev_16_0089.html)