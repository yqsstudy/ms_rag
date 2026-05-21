---
title: "sanitizerRtMemsetAsync"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0054.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0054.html"
---

# sanitizerRtMemsetAsync

#### 功能说明

调用aclrtMemsetAsync接口初始化内存，将内存中的内容设置为指定的值，并向检测工具上报内存初始化信息。此接口为异步接口。实际的内存初始化行为和参数含义与aclrtMemsetAsync一致。

可参见章节查看aclrtMemsetAsync的详细说明。

#### 函数原型

```
aclError sanitizerRtMemsetAsync(void *devPtr, size_t maxCount, int32_t value, size_t count, aclrtStream stream, char const *filename, int lineno);
```

#### 参数说明
**表1**参数说明
参数名

输入/输出

描述

devPtr

输入

内存起始地址的指针。

maxCount

输入

内存的最大长度，单位为Byte。

value

输入

初始化内存的指定值。

count

输入

初始化内存的长度，单位为Byte。

stream

输入

指定的stream。

filename

输入

内存初始化被调用处的文件名。

lineno

输入

内存初始化被调用处的行号。
|  |  |  |
| --- | --- | --- |
|  |  |  |
|  |  |  |
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