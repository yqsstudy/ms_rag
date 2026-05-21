---
title: "mstxMemHeapUnregister"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/API/mstxAPIReference/atlasopdev_16_0146.html"
date_collected: "2026-05-04"
category: "mstx_api"
original_path: "zh/mindstudio/830/API/mstxAPIReference/atlasopdev_16_0146.html"
---

# mstxMemHeapUnregister

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

注销内存池时，与之关联的Regions将一并被注销。

#### 函数原型

```
void mstxMemHeapUnregister(mstxDomainHandle_t domain, mstxMemHeapHandle_t heap)
```

#### 参数说明
**表1**参数说明
参数

输入/输出

说明

domain

输入

[domain为内存池所属的域，为globalDomain或mstxDomainCreateA](msprof_tx_0006.html)返回的句柄。

数据类型：const char *。

heap

输入

[heap为需要注销内存池的句柄，为mstxMemHeapRegister](atlasopdev_16_0145.html)的返回值。

```
struct mstxMemHeap_st;
typedef struct mstxMemHeap_st mstxMemHeap_t; 
typedef mstxMemHeap_t* mstxMemHeapHandle_t;
```
|  |  |  |
| --- | --- | --- |
|  |  |  |
|  |  |  |

#### 返回值

无

#### 调用示例

```
mstxMemHeapDesc_t heapDesc{};
mstxMemHeapHandle_t memPool = mstxMemHeapRegister(globalDomain, &heapDesc); // 注册内存池
...
mstxMemHeapUnregister(globalDomain, memPool);                        // 注销内存池
```