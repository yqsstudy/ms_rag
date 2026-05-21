---
title: "mstxMemHeapRegister"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/API/mstxAPIReference/atlasopdev_16_0145.html"
date_collected: "2026-05-04"
category: "mstx_api"
original_path: "zh/mindstudio/830/API/mstxAPIReference/atlasopdev_16_0145.html"
---

# mstxMemHeapRegister

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

注册内存池。用户在调用该接口注册内存池时，需确保该内存已提前申请。

#### 函数原型

```
mstxMemHeapHandle_t mstxMemHeapRegister(mstxDomainHandle_t domain, mstxMemHeapDesc_t const *desc)
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

```
typedef enum mstxMemHeapUsageType {
    /* @brief 此堆内存作为内存池使用
     * 使用此使用方式注册的堆内存，需要使用二次分配注册后才可以访问
     */
    MSTX_MEM_HEAP_USAGE_TYPE_SUB_ALLOCATOR = 0,
} mstxMemHeapUsageType;

/** @brief 堆内存的类型
 * 此处的“类型”是指通过何种方式来描述堆内存指针。当前仅支持线性排布的
 * 内存，但此处保留日后支持更多内存类型的扩展能力。比如某些API返回
 * 多个句柄来描述内存范围，或者一些高维内存需要使用stride、tiling或
 * interlace来描述
 */
typedef enum mstxMemType {
    /** @brief 标准线性排布的虚拟内存
      * 此时mstxMemHeapRegister接收mstxMemVirtualRangeDesc_t类型的描述
      */
    MSTX_MEM_TYPE_VIRTUAL_ADDRESS = 0,
} mstxMemType;

typedef struct mstxMemVirtualRangeDesc_t {
    uint32_t deviceId;  // 内存区域对应的设备 ID
    void const *ptr;  // 内存区域的起始地址
    uint64_t size;  // 内存区域的长度
} mstxMemVirtualRangeDesc_t;

typedef struct mstxMemHeapDesc_t {
    mstxMemHeapUsageType usage;  // 堆内存的使用方式
    mstxMemType type;  // 堆内存的类型
    void const *typeSpecificDesc;  // 堆内存在指定内存类型下的描述信息
} mstxMemHeapDesc_t;
```
|  |  |  |
| --- | --- | --- |
|  |  |  |
|  |  |  |

#### 返回值

内存池对应的句柄。

#### 调用示例

```
mstxMemVirtualRangeDesc_t rangeDesc = {};
    rangeDesc.deviceId = deviceId;       // 设备编号
    rangeDesc.ptr = gm;                  // 注册的内存池gm首地址
    rangeDesc.size = 1024;               // 内存池大小
    heapDesc.typeSpecificDesc = &rangeDesc;
    mstxMemHeapDesc_t heapDesc{};
    mstxMemHeapHandle_t memPool = mstxMemHeapRegister(globalDomain, &heapDesc); // 注册内存池  
```