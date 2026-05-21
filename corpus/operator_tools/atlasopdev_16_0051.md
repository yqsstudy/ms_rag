---
title: "sanitizerRtMallocCached"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0051.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0051.html"
---

# sanitizerRtMallocCached

#### 功能说明

调用aclrtMallocCached接口在Device上申请size大小的线性内存，通过*devPtr返回已分配内存的指针，并向检测工具上报内存分配信息。该接口在任何场景下，申请的内存都支持cache缓存。实际的内存分配行为和参数含义与aclrtMallocCached一致。

可参见章节查看aclrtMallocCached的详细说明。

#### 函数原型

```
aclError sanitizerRtMallocCached(void **devPtr, size_t size, aclrtMemMallocPolicy policy, char const *filename, int lineno);
```

#### 参数说明
**表1**参数说明
参数名

输入/输出

描述

devPtr

输出

指向“Device上已分配内存的指针”的指针。

size

输入

申请内存的大小，单位为Byte。

size不能为0。

policy

输入

内存分配规则。

filename

输入

内存分配被调用处的文件名。

lineno

输入

内存分配被调用处的行号。
|  |  |  |
| --- | --- | --- |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |

#### 返回值

返回0表示成功，返回其它值表示失败。

#### 调用示例

[具体操作请参见使用示例的步骤4](atlasopdev_16_0047.html#ZH-CN_TOPIC_0000002505040574__zh-cn_topic_0000002502746432_zh-cn_topic_0000001748761501_li1423525185711)。
**父主题：**[sanitizer接口](atlasopdev_16_0141.html)