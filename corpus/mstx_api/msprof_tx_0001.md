---
title: "接口简介"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/API/mstxAPIReference/msprof_tx_0001.html"
date_collected: "2026-05-04"
category: "mstx_api"
original_path: "zh/mindstudio/830/API/mstxAPIReference/msprof_tx_0001.html"
---

# 接口简介

本节介绍mstx打点接口。可以自定义采集时间段或者关键函数的开始和结束时间点，识别关键函数或迭代等信息，对性能和算子问题快速定界。

默认情况下mstx API无任何功能，需要在用户应用程序中调用mstx API后，根据不同场景使能mstx打点功能，例如使用msprof命令行采集时配置--msproftx=on、使用AscendCL API采集时配置ACL_PROF_MSPROFTX以及Ascend PyTorch Profiler接口采集时配置mstx=True等。

- **库文件libms_tools_ext.so路径：${INSTALL_DIR}**/lib64/。
- **使用头文件编译时，用户程序编译时需链接dl库。头文件ms_tools_ext.h路径：${INSTALL_DIR}**/include/mstx。

${INSTALL_DIR}请替换为CANN软件安装后文件存储路径。以root用户安装为例，则安装后文件存储路径为：/usr/local/Ascend/cann。

#### 接口列表
**表1**MindStudio mstx接口列表
接口名称

功能简介

[mstxGetToolId](atlasopdev_16_0187.html)

用于获取当前劫持mstx接口的工具ID。

[mstxMarkA](msprof_tx_0003.html)

标识瞬时事件。

[mstxRangeStartA](atlasopdev_16_0117.html)

标识时间段事件的开始。

[mstxRangeEnd](atlasopdev_16_0118.html)

标识时间段事件的结束。

[mstxDomainCreateA](msprof_tx_0006.html)

创建自定义domain。

[mstxDomainDestroy](msprof_tx_0007.html)

销毁指定的domain，销毁后的domain不能再次使用，需要重新创建。

[mstxDomainMarkA](msprof_tx_0008.html)

在指定的domain内，标记瞬时事件。

[mstxDomainRangeStartA](msprof_tx_0009.html)

在指定的domain内，标识时间段事件的开始。

[mstxDomainRangeEnd](msprof_tx_0010.html)

在指定的domain内，标识时间段事件的结束。

[mstxMemHeapRegister](atlasopdev_16_0145.html)

注册内存池。

[mstxMemRegionsRegister](atlasopdev_16_0147.html)

注册内存池二次分配。

[mstxMemRegionsUnregister](atlasopdev_16_0148.html)

注销内存池二次分配。

[mstxMemHeapUnregister](atlasopdev_16_0146.html)

注销内存池时，与之关联的Regions将一并被注销。
|  |  |
| --- | --- |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |