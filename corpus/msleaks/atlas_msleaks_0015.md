---
title: "低效内存识别"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/msleaks/atlas_msleaks_0015.html"
date_collected: "2026-05-04"
category: "msleaks"
original_path: "zh/mindstudio/830/T&ITools/msleaks/atlas_msleaks_0015.html"
---

# 低效内存识别

在训练推理模型时，可能会存在部分内存块申请后没有立即使用，或者使用结束后未及时释放等情况，从而导致内存使用增高的现象，对于内存来说，这种现象是低效的。

低效内存（Inefficient Memory）是指在模型运行过程中，某个Tensor对象在Device侧有关内存申请、释放以及访问操作的时机不合理。

**msLeaks工具针对op算子粒度支持过早申请****（Early Allocation）、过迟释放****（Late Deallocation）、临时闲置**（Temporary Idleness）三种低效内存的识别能力，具体说明如表1所示。
**表1**低效内存说明
分类

说明

过早申请

对于某个Tensor对象，在其申请内存的算子与第一次访问的算子之间，存在着其他算子包含了其他Tensor对象的释放操作，这个Tensor对象就是过早申请了。

过迟释放

对于某个Tensor对象，在其最后一次访问的算子与释放内存的算子之间，存在着其他算子包含了其他Tensor对象的申请操作，这个Tensor对象就是过迟释放了。

临时闲置

对于某个Tensor对象，其任意两次内存访问操作的算子之间，存在超过某个阈值的算子数量，则这个对象即为临时闲置对象。
|  |  |
| --- | --- |
|  |  |
|  |  |
|  |  |

#### 在线方式

执行以下命令，开启低效内存识别功能。其中Application为用户脚本。
**
```
msleaks ${Application} --analysis=inefficient --events=alloc,free,access,launch
```

- 当使用低效内存识别功能时，需设置--events=access,alloc,free,launch。
- msLeaks工具仅支持识别ATB LLM和Ascend Extension for PyTorch单算子场景的低效内存。

#### 离线方式

[低效内存识别可通过接口自定义设置，具体操作可参见API参考](atlas_msleaks_0017.html#ZH-CN_TOPIC_0000002538348383)。

#### 结果说明

*低效内存识别的结果会保存在leaks_dump_{timestamp*[}.csv文件中，具体信息可参见输出说明](atlas_msleaks_0016.html#ZH-CN_TOPIC_0000002506628524)。
**父主题：**[内存分析](atlas_msleaks_0004.html)