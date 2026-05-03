---
title: 性能问题案例
source: https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_052.html?framework=pytorch
date_collected: 2026-04-29
---

# 性能问题案例

> 来源: [https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_052.html?framework=pytorch](https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_052.html?framework=pytorch)

# Host Bound问题分类

#### Host Bound问题简介

在torch_npu训练和推理场景中，Host侧（CPU）的任务下发（如算子调度、内存分配）与Device侧（NPU）的任务执行是异步进行的。当Host侧任务下发耗时超过Device侧任务执行耗时，Device会因等待新任务而处于空闲状态，形成性能瓶颈，即Host Bound问题。

#### Host Bound问题表现

  1. 算子下发连线呈现垂直密集状态，表明NPU在等待CPU下发任务。
  2. 因等待导致NPU闲置时间（Free time）占比过高。

**图1** 典型Host Bound场景性能数据  
![](images/toolsample6_052_zh-cn_image_0000002503927358.png)




#### Host Bound问题优化方法

Host Bound问题主要由算子下发延迟、CPU计算负载过重两个因素导致，可采用表1方法进行优化。

**表1** Host Bound常见优化手段优化方法 | 优势 | 说明  
---|---|---  
算子下发优化 | 减少算子下发次数 | 通过[快慢卡问题定位方法](https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_030.html?framework=pytorch)识别瓶颈点后，采用逻辑优化、等价计算替换和算子融合等方法进行优化（参考[亲和算子优化策略](https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_050.html?framework=pytorch)）。  
提升算子下发速度 | 

  * [流水优化](https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_054.html?framework=pytorch)：是一种通用且高效的优化手段，其核心是将部分算子适配任务迁移至二级流水，从而均衡两级流水负载并降低任务出队唤醒耗时。
  * [绑核优化](https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_058.html?framework=pytorch)：通过控制CPU端算子任务的处理器亲和性（即绑核），优化任务执行效率，避免跨NUMA（非统一内存访问架构）节点的内存访问，降低任务调度开销。
  * [编译优化](https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_062.html?framework=pytorch)：通过应用毕昇编译器（BiSheng Compiler）的LTO（链接时优化）和PGO（配置文件引导优化）技术，对Python、PyTorch（torch）及其昇腾扩展（torch_npu/Ascend Extension for PyTorch）三个核心组件进行源码编译构建，可有效提升程序性能。

  
CPU计算优化 | 发挥异构算力优势 | 尽量减少AI CPU算子的使用，优先选用亲和性更优的算子，可参考[亲和算子优化策略](https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_050.html?framework=pytorch)）。  
发挥并行计算优势 | 促进CPU与NPU的异步并行处理（例如，将数据处理逻辑置于DataLoader中），并减少流同步操作（如谨慎使用item(), cpu(), npu() 等操作，尽量合并或避免使用）。  
  
此外，存在一类属于下发异常问题，即算子下发过程因为资源抢占、操作系统调度策略冲突等因素导致耗时显著增加，参考[下发异常分析](https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_075.html?framework=pytorch)。

**父主题：** [Host Bound问题定位及解决方法](https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_052.html?framework=pytorch)
