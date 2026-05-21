---
title: "mstx扩展功能"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0142.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0142.html"
---

# mstx扩展功能

#### mstx接口简介

[mstx接口是MindStudio提供的一套扩展接口，它允许用户在应用程序中插入特定的标记，以便在工具进行内存检测时能够更精确地定位特定算子的内存问题。例如，针对二级指针类算子，在不使能mstx接口的情况下，得到的地址空间可能不准确。通过《MindStudio mstx API参考](https://www.hiascend.com/document/detail/zh/mindstudio/830/API/mstxAPIReference/msprof_tx_0001.html)[》的mstxMemRegionsRegister](https://www.hiascend.com/document/detail/zh/mindstudio/830/API/mstxAPIReference/atlasopdev_16_0147.html)[和mstxMemRegionsUnregister](https://www.hiascend.com/document/detail/zh/mindstudio/830/API/mstxAPIReference/atlasopdev_16_0148.html)接口，可以将准确的地址空间传递给异常检测工具，实现更精准的内存检测。

[Kernel直调](atlasopdev_16_0039.html#ZH-CN_TOPIC_0000002505040558__zh-cn_topic_0000002534426413_zh-cn_topic_0000001691887174_li12291456391)中的内核调用符场景暂不支持使用mstx接口。

#### mstx接口列表

msSanitizer工具调用的mstx接口列表如表1[所示，具体使用状况请参考《MindStudio mstx API参考](https://www.hiascend.com/document/detail/zh/mindstudio/830/API/mstxAPIReference/msprof_tx_0001.html)》。
**表1**msSanitizer工具调用的mstx接口列表
接口名称

功能简介

mstxDomainCreateA

创建一个新的mstx域。

mstxMemHeapRegister

注册内存池。用户在调用该接口注册内存池时，需确保该内存已提前申请。

mstxMemRegionsRegister

注册内存池二次分配。用户需保证RegionsRegister的内存位于mstxMemHeapRegister注册的范围内，否则工具会提示越界读写。

mstxMemRegionsUnregister

注销内存池二次分配。

mstxMemHeapUnregister

注销内存池时，与之关联的Regions将一并被注销。
|  |  |
| --- | --- |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |

#### mstx接口的使用

- msSanitizer工具默认使能mstx接口，允许用户使用mstx接口自定义算子使用的内存空间地址和大小，可识别并快速界定算子的内存问题。
- [mstx当前提供了两种API的使用方式：库文件和头文件，以Link](https://gitee.com/ascend/samples/tree/master/operator/ascendc/0_introduction/1_add_frameworklaunch/AclNNInvocation)为例：
  - 此样例工程不支持Atlas A3 训练系列产品。

  - 在${git_clone_path}/samples/operator/ascendc/0_introduction/1_add_frameworklaunch/AclNNInvocation/src/CMakeLists.txt路径下新增库文件libms_tools_ext.so，地址为：${INSTALL_DIR}/lib64/libms_tools_ext.so。********
```
# Header path
include_directories(
     ...
    ${CUST_PKG_PATH}/include
)
...
target_link_libraries( 
    ...
    dl
)
```

  - 在${git_clone_path}/samples/operator/ascendc/0_introduction/1_add_frameworklaunch/AclNNInvocation/src/main.cpp路径下，将用户程序编译链接dl库，对应的头文件ms_tools_ext.h地址：${INSTALL_DIR}/include/mstx。****
```
...
#include "mstx/ms_tools_ext.h"
...
```

${INSTALL_DIR}请替换为CANN软件安装后文件存储路径。以root用户安装为例，则安装后文件存储路径为：/usr/local/Ascend/cann。

#### 调用示例

```
mstxMemVirtualRangeDesc_t rangeDesc = {};
    rangeDesc.deviceId = deviceId;       // 设备编号
    rangeDesc.ptr = gm;                  // 注册的内存池CM首地址
    rangeDesc.size = 1024;               // 内存池大小
    heapDesc.typeSpecificDesc = &rangeDesc;
    mstxMemHeapDesc_t heapDesc{};
    mstxMemHeapHandle_t memPool = mstxMemHeapRegister(globalDomain, &heapDesc); // 注册内存池
    mstxMemVirtualRangeDesc_t rangesDesc[1] = {};                // 二次分配包含的region数量
    mstxMemRegionHandle_t regionHandles[1] = {};
    rangesDesc[0].deviceId = deviceId;                           // 设备编号
    rangesDesc[0].ptr = gm;                                      // 二次分配GM地址
    rangesDesc[0].size = 256;                                    // 二次分配大小
    mstxMemRegionsRegisterBatch_t regionsDesc{};
    regionsDesc.heap = memPool;
    regionsDesc.regionType = MSTX_MEM_TYPE_VIRTUAL_ADDRESS;
    regionsDesc.regionCount = 1;
    regionsDesc.regionDescArray = rangesDesc;
    regionsDesc.regionHandleArrayOut = regionHandles;
    mstxMemRegionsRegister(globalDomain, ®ionsDesc);              // 二次分配注册
    Do(blockDim, nullptr, stream, gm);                            // 算子Kernel函数
    mstxMemRegionRef_t regionRef[1] = {};
    regionRef[0].refType = MSTX_MEM_REGION_REF_TYPE_HANDLE;
    regionRef[0].handle = regionHandles[0];
    mstxMemRegionsUnregisterBatch_t refsDesc = {};
    refsDesc.refCount = 1;
    refsDesc.refArray = regionRef;
    mstxMemRegionsUnregister(globalDomain, &refsDesc);                   // 注销二次分配
    mstxMemHeapUnregister(globalDomain, memPool);                        // 注销内存池
```
**父主题：**[对外接口使用说明](atlasopdev_16_0048.html)