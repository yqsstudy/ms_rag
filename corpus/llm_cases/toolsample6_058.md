---
title: "绑核优化"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_058.html"
date_collected: "2026-05-04"
category: "llm_cases"
original_path: "zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_058.html"
---

# 绑核优化

#### 使能说明

通过设置以下环境变量启用该特性，适用于任务自主调度能力不足或快慢卡问题突出的网络场景。

```
export CPU_AFFINITY_CONF=<mode>,npu<value1>:<value2>-<value3>
```

- **<mode>：绑核模式**。配置为 “0”或未配置时禁用绑核；配置为 “1” 启用粗粒度绑核；配置为 “2”启用细粒度绑核。
- **npu<value1>:<value2>-<value3>：自定义绑核区间**。当前仅在 <mode> 配置不为“0”时生效。<value1> 表示 NPU 卡编号，<value2>-<value3> 指定该卡进程的 CPU 核心绑定区间。

#### 详细原理

- **粗粒度绑核**：将单张NPU卡关联的所有线程绑定至指定CPU核心区间。
- **细粒度绑核**：将单张NPU卡关联的主要线程绑定至指定CPU核心区间，每个线程独占一个核心，实现相互隔离。

#### 配置示例

1. 启用粗粒度绑核。

```
export CPU_AFFINITY_CONF=1
```

2. 启用细粒度绑核。

```
export CPU_AFFINITY_CONF=2
```

3. 启用自定义绑核。

```
export CPU_AFFINITY_CONF=1,npu0:0-1,npu1:2-5,npu3:6-6
```

4. 执行上述配置后，NPU卡绑定详情如下所示。

  - NPU 0 卡进程绑定至CPU核心 0-1。
  - NPU 1 卡进程绑定至CPU核心 2-5。
  - NPU 3 卡进程绑定至CPU核心 6。
  - 其他NPU卡进程使用默认核心区间。

**父主题：**[Host Bound问题定位及解决方法](toolsample6_052.html)