---
title: "mstxMemRegionsRegister"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/API/mstxAPIReference/atlasopdev_16_0147.html"
date_collected: "2026-05-04"
category: "mstx_api"
original_path: "zh/mindstudio/830/API/mstxAPIReference/atlasopdev_16_0147.html"
---

# mstxMemRegionsRegister

#### 产品支持情况

产品

是否支持

Atlas A3 训练系列产品/Atlas A3 推理系列产品

√

Atlas A2 训练系列产品/Atlas A2 推理系列产品

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

[注册内存池二次分配。用户需保证RegionsRegister的内存位于mstxMemHeapRegister](atlasopdev_16_0145.html)注册的范围内，否则工具会提示越界读写。

#### 函数原型

```
void mstxMemRegionsRegister(mstxDomainHandle_t domain, mstxMemRegionsRegisterBatch_t const *desc)
```

#### 参数说明
**表1**参数说明
参数

输入/输出

说明

domain

输入

[为globalDomain或mstxDomainCreateA](msprof_tx_0006.html)返回的句柄。

数据类型：const char *。

desc

输入

内存池待二次分配的内存区域描述信息，不能为空。

```
struct mstxMemRegion_st;
typedef struct mstxMemRegion_st mstxMemRegion_t;
typedef mstxMemRegion_t* mstxMemRegionHandle_t;

typedef struct mstxMemRegionsRegisterBatch_t {
    mstxMemHeapHandle_t heap;  // 要进行二次分配的内存池句柄
    mstxMemType regionType;  // 内存区域的内存类型
    size_t regionCount;  // 内存区域的个数
    void const *regionDescArray;  // 内存区域描述数据
    mstxMemRegionHandle_t* regionHandleArrayOut;  // 返回的注册二次分配得到的句柄数组
} mstxMemRegionsRegisterBatch_t;
```
|  |  |  |
| --- | --- | --- |
|  |  |  |
|  |  |  |

#### 返回值

无

#### 调用示例

```
mstxMemRegionsRegisterBatch_t regionsDesc{};
regionsDesc.heap = memPool;
regionsDesc.regionType = MSTX_MEM_TYPE_VIRTUAL_ADDRESS;
regionsDesc.regionCount = 1;
regionsDesc.regionDescArray = rangesDesc;
regionsDesc.regionHandleArrayOut = regionHandles;
mstxMemRegionsRegister(globalDomain, ®ionsDesc);              // 二次分配注册 
```