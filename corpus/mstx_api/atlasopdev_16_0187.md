---
title: "mstxGetToolId"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/API/mstxAPIReference/atlasopdev_16_0187.html"
date_collected: "2026-05-04"
category: "mstx_api"
original_path: "zh/mindstudio/830/API/mstxAPIReference/atlasopdev_16_0187.html"
---

# mstxGetToolId

#### 产品支持情况

产品

是否支持

Atlas A3 训练系列产品
 /
 Atlas A3 推理系列产品

√

Atlas A2 训练系列产品
 /
 Atlas A2 推理系列产品

√

Atlas 200I/500 A2 推理产品

√

Atlas 推理系列产品

√

Atlas 训练系列产品

√
|  |  |
| --- | --- |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |

#### 功能说明

用于获取当前劫持mstx接口的工具ID，工具ID宏定义如下：
[](https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0008.html)[](https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0021.html)[](/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0081.html)[](/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0038.html)[](/document/detail/zh/mindstudio/830/T&ITools/msleaks/atlas_msleaks_0001.html)
```
#define MSTX_TOOL_INVALID_ID 0x0         // 无效值0，表示无工具拉起程序
#define MSTX_TOOL_MSPROF_ID 0x1000       // 0x1000，表示程序由《msprof模型调优工具》或《MSPTI调优工具》工具拉起
#define MSTX_TOOL_MSOPPROF_ID 0x1001     // 0x1001，表示程序由算子调优（msProf）工具拉起
#define MSTX_TOOL_MSSANITIZER_ID 0x1002  // 0x1002，表示程序由异常检测（msSanitizer）工具拉起
#define MSTX_TOOL_MSLEAKS_ID 0x1003      // 0x1003，表示程序由《msLeaks内存泄漏检测工具》拉起
```

#### 函数原型

```
void mstxGetToolId(uint64 *id)
```

#### 参数说明
**表1**参数说明
参数

输入/输出

说明

id

输出

作为出参，返回当前劫持mstx接口的工具ID。

数据类型：uint64 *。
|  |  |  |
| --- | --- | --- |
|  |  |  |

#### 返回值

无

#### 调用示例

```
uint64 id;
mstxGetToolId(&id);
```