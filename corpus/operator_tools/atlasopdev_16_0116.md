---
title: "msDebug工具断点设置在核函数内，命中断点后执行continue命令，算子运行失败"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0116.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0116.html"
---

# msDebug工具断点设置在核函数内，命中断点后执行continue命令，算子运行失败

#### 现象描述

打印信息Synchronize stream failed. error code is 507035，查看plog显示aic error code=0x8000000000000000，并且在命中断点时使用ascend info cores命令可以看到当前核的PC值与预期不符。

#### 原因分析

Kernel函数中workspace入参的空间大小在Tiling函数中被设置为0，经过单算子API调用后变成一个非法地址。虽然workspace入参在Kernel函数未被使用，调试器展示Kernel入参时也会对workspace指针进行解引用，导致算子运行错误。

#### 解决措施

[参考Host侧Tiling实现](https://www.hiascend.com/document/detail/zh/canncommercial/850/opdevg/Ascendcopdevg/atlas_ascendc_10_00021.html)将workspacesize从0设置成预留内存大小。API在计算过程需要一些workspace内存作为缓存，因此算子Tiling函数需要为API预留workspace内存，预留内存大小通过GetLibApiWorkSpaceSize接口获取。参考如下代码：

```
1
2
3
4
5
```

```
#include "tiling/platform/platform_ascendc.h"
auto ascendcPlatform = platform_ascendc::PlatformAscendC(context->GetPlatformInfo());
size_t systemWorkspaceSize = ascendcPlatform.GetLibApiWorkSpaceSize();
size_t*currentWorkspace = context->GetWorkspaceSizes(1); //只使用1块Workspace
currentWorkspace[0]= systemWorkspaceSize;

```
|  |  |
| --- | --- |
**父主题：**[FAQ](atlasopdev_16_0077.html)