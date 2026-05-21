---
title: "mstxMemRegionsUnregister"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/API/mstxAPIReference/atlasopdev_16_0148.html"
date_collected: "2026-05-04"
category: "mstx_api"
original_path: "zh/mindstudio/830/API/mstxAPIReference/atlasopdev_16_0148.html"
---

# mstxMemRegionsUnregister

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

注销内存池二次分配。

#### 函数原型

```
void mstxMemRegionsUnregister(mstxDomainHandle_t domain, mstxMemRegionsUnregisterBatch_t const *desc)
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

[输入的描述信息必须是某一次mstxMemHeapRegister](atlasopdev_16_0145.html)的输入描述信息，否则工具将打印提示错误。

```
typedef enum mstxMemRegionRefType {
    // 通过指针描述内存引用
    MSTX_MEM_REGION_REF_TYPE_POINTER = 0,
    // 通过句柄描述内存引用
    MSTX_MEM_REGION_REF_TYPE_HANDLE
} mstxMemRegionRefType;

typedef struct mstxMemRegionRef_t {
    mstxMemRegionRefType refType; // 描述内存引用的方式
    union {
        void const* pointer;  // 当前内存引用通过指针描述时，此处保存内存区域指针
        mstxMemRegionHandle_t handle;  // 当内存引用通过句柄描述时，此处保存内存区域的句柄 
    };
} mstxMemRegionRef_t;

typedef struct mstxMemRegionsUnregisterBatch_t {
    size_t refCount;  // 内存引用的个数
    mstxMemRegionRef_t const *refArray;  // 要注销的内存区域引用
} mstxMemRegionsUnregisterBatch_t;
```
|  |  |  |
| --- | --- | --- |
|  |  |  |
|  |  |  |

#### 返回值

无

#### 调用示例

```
mstxMemRegionsUnregisterBatch_t refsDesc = {}
refsDesc.refCount = 1;
refsDesc.refArray = regionRef;
mstxMemRegionsUnregister(globalDomain, &refsDesc);                   // 注销二次分配
```