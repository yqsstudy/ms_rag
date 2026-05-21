---
title: "接口列表"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0150.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0150.html"
---

# 接口列表

#### 接口简介

[msSanitizer工具包含sanitizer接口和mstx扩展接口两种类型。sanitizer接口用于CANN软件栈的检测，与ACL系列接口一一对应。此类接口会在ACL对应接口的功能基础上，额外向工具上报接口调用位置的代码文件和行号信息，使用时需导入sanitizer API头文件和链接动态库，具体请参见导入API头文件和链接动态库](atlasopdev_16_0047.html#ZH-CN_TOPIC_0000002505040574__zh-cn_topic_0000002502746432_section1587150123812)[。mstx扩展接口用于用户自定义上报内存池信息，以实现更准确的检测，具体请参见mstx扩展功能](atlasopdev_16_0142.html#ZH-CN_TOPIC_0000002504880768)。
**表1**msSanitizer工具接口列表
接口类型

接口名称

功能简介

[sanitizer接口](atlasopdev_16_0141.html#ZH-CN_TOPIC_0000002504880756)

sanitizerRtMalloc

在ACL对应接口的功能基础上，向msSanitizer工具上报sanitizer接口调用位置的代码文件和行号信息。

sanitizerRtMallocCached

sanitizerRtFree

sanitizerRtMemset

sanitizerRtMemsetAsync

sanitizerRtMemcpy

sanitizerRtMemcpyAsync

sanitizerRtMemcpy2d

sanitizerRtMemcpy2dAsync

sanitizerReportMalloc

sanitizerReportFree

[mstx扩展功能](atlasopdev_16_0142.html#ZH-CN_TOPIC_0000002504880768)

mstxDomainCreateA

创建域。

mstxMemHeapRegister

内存池注册接口。

mstxMemHeapUnregister

内存池注销接口。

mstxMemRegionsRegister

内存池二次分配注册接口。

mstxMemRegionsUnregister

内存池二次分配注销接口。
|  |  |  |
| --- | --- | --- |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
**父主题：**[对外接口使用说明](atlasopdev_16_0048.html)