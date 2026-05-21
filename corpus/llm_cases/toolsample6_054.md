---
title: "流水优化"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_054.html"
date_collected: "2026-05-04"
category: "llm_cases"
original_path: "zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_054.html"
---

# 流水优化

#### 使能说明

通过设置以下环境变量启用该特性，通常适用于Host Bound问题严重的网络场景。

```
export TASK_QUEUE_ENABLE=2
```

#### 详细原理

[task_queue算子下发队列支持三个配置级别（以add算子为例），用户可以根据需要自行配置，详细介绍请参见《Ascend Extension for PyTorch 环境变量参考](https://www.hiascend.com/document/detail/zh/Pytorch/730/comref/Envvariables/docs/zh/environment_variable_reference/env_variable_list.md)[》的“TASK_QUEUE_ENABLE](https://www.hiascend.com/document/detail/zh/Pytorch/730/comref/Envvariables/docs/zh/environment_variable_reference/TASK_QUEUE_ENABLE.md)”章节。

#### 注意事项

- [当ASCEND_LAUNCH_BLOCKING设置为"1"时，task_queue算子队列将被强制关闭，此时TASK_QUEUE_ENABLE配置失效，ASCEND_LAUNCH_BLOCKING的配置可参见《Ascend Extension for PyTorch 环境变量参考](https://www.hiascend.com/document/detail/zh/Pytorch/730/comref/Envvariables/docs/zh/environment_variable_reference/env_variable_list.md)[》的“ASCEND_LAUNCH_BLOCKING](https://www.hiascend.com/document/detail/zh/Pytorch/730/comref/Envvariables/docs/zh/environment_variable_reference/ASCEND_LAUNCH_BLOCKING.md)”章节。

- 配置 TASK_QUEUE_ENABLE=2 时，由于内存访问并发性增加，可能导致运行期间 NPU 内存峰值上升。
**父主题：**[Host Bound问题定位及解决方法](toolsample6_052.html)