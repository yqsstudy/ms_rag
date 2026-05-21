---
title: "MSPTI样例集"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0024.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0024.html"
---

# MSPTI样例集

本节提供MSPTI各种接口的使用样例，供用户理解使用MSPTI接口，样例具体说明及目录如下。

#### 前提条件

- 请确保安装CANN Toolkit开发套件包和ops算子包。
[参见《CANN 软件安装指南](https://www.hiascend.com/document/detail/zh/canncommercial/850/softwareinst/instg/instg_0000.html?Mode=PmIns&InstallType=local&OS=openEuler)》。

- MSPTI Python API部分的样例依赖于PyTorch框架和torch_npu插件，请确保安装。
[参见《Ascend Extension for PyTorch 软件安装指南](https://www.hiascend.com/document/detail/zh/Pytorch/730/configandinstg/instg/docs/zh/installation_guide/installation_description.md)[》中的“安装PyTorch](https://www.hiascend.com/document/detail/zh/Pytorch/730/configandinstg/instg/docs/zh/installation_guide/installation_via_binary_package.md)”。

#### 构建样例执行

1. ***安装CANN软件后，使用CANN运行用户进行编译、运行时，需要以CANN运行用户登录环境，执行source ${install_path}*/set_env.sh**命令设置环境变量。其中${install_path}为CANN软件的安装目录，例如：/usr/local/Ascend/ascend-toolkit。
2. 进入样例目录。
MSPTI样例代码集成在CANN Toolkit开发套件包和ops算子包中，路径为${INSTALL_DIR}/tools/mspti/samples。

${INSTALL_DIR}请替换为CANN软件安装后文件存储路径。若安装的Ascend-cann-toolkit软件包，以root安装举例，则安装后文件存储路径为：/usr/local/Ascend/ascend-toolkit/latest。

示例如下：

```
cd ${INSTALL_DIR}/tools/mspti/samples/callback_domain
```

3. 执行对应样例目录下的sample_run.sh。
```
bash sample_run.sh
```

下表为当前提供的样例介绍：
**表1**Callback API样例
样例

说明

产品支持情况

callback_domain

展示Callback API功能，可以通过msptiEnableDomain，在runtime API的前后执行Callback操作。

Atlas A2 训练系列产品/Atlas A2 推理系列产品

Atlas A3 训练系列产品/Atlas A3 推理系列产品

callback_mstx

1. 展示Callback与mstx接口相结合功能, 使用Callback API和mstx打点功能，在runtime的launch Kernel前后打点，采集算子数据。
2. 演示Callback中userdata用法，用户可以通过userdata透传配置或者部分运行参数。

Atlas A2 训练系列产品/Atlas A2 推理系列产品

Atlas A3 训练系列产品/Atlas A3 推理系列产品
|  |  |  |
| --- | --- | --- |
|  |  |  |
|  |  |  |
**表2**Activity API样例
样例

说明

产品支持情况

mspti_activity

1. 展示Activity API接口的基本功能，样例展示如何采集Kernel和Memory等数据。
2. 演示Activity API的基本运行，讲述Activity API的基本使用，包括Activity Buffer内存分配，Buffer消费等逻辑。

Atlas A2 训练系列产品/Atlas A2 推理系列产品

Atlas A3 训练系列产品/Atlas A3 推理系列产品

mspti_correlation

1. 展示Activity API接口的基本功能，展示如何通过correlationId字段将API和Kernel数据做关联。
2. 演示runtime API下发与Kernel实际执行数据的关联，关联后可以将算子的下发和执行一一对应，方便分析性能瓶颈。

Atlas A2 训练系列产品/Atlas A2 推理系列产品

Atlas A3 训练系列产品/Atlas A3 推理系列产品

mspti_external_correlation

1. 展示MSPTI External Correlation功能。
2. 演示msptiActivityPopExternalCorrelationId和msptiActivityPushExternalCorrelationId两接口使用方法，用户可以通过接口将各种API关联到一起，方便回溯函数的调用栈。

Atlas A2 训练系列产品/Atlas A2 推理系列产品

Atlas A3 训练系列产品/Atlas A3 推理系列产品

mspti_hccl_activity

展示Activity API接口的基本功能，样例展示如何采集HCCL通信数据。

Atlas A2 训练系列产品/Atlas A2 推理系列产品

Atlas A3 训练系列产品/Atlas A3 推理系列产品

mspti_mstx_activity_domain

1. 展示MSPTI控制mstxDomain功能，通过开关控制打点数据是否采集。
2. 用户可以通过MSPTI开关实时开关采集打点，减小性能损耗。

Atlas A2 训练系列产品/Atlas A2 推理系列产品

Atlas A3 训练系列产品/Atlas A3 推理系列产品
|  |  |  |
| --- | --- | --- |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
**表3**Python API样例
样例

说明

产品支持情况

python_monitor

展示Monitor基本使用方式，通过KernelMonitor、HcclMonitor获取计算算子和通信算子的耗时。

Atlas A2 训练系列产品/Atlas A2 推理系列产品

Atlas A3 训练系列产品/Atlas A3 推理系列产品

python_mstx_monitor

展示MstxMonitor基本使用方式，用户可以通过Mstx打点采集对应算子（如matmul）耗时。

Atlas A2 训练系列产品/Atlas A2 推理系列产品

Atlas A3 训练系列产品/Atlas A3 推理系列产品
|  |  |  |
| --- | --- | --- |
|  |  |  |
|  |  |  |
**父主题：**[MSPTI调优工具](atlasprofiling_16_0020.html)