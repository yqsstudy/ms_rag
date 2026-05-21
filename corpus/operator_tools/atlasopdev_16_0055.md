---
title: "sanitizerRtMemcpy"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0055.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0055.html"
---

# sanitizerRtMemcpy

#### 功能说明

调用aclrtMemcpy接口完成内存复制，并向检测工具上报内存复制信息。实际的内存复制行为和参数含义与aclrtMemcpy一致。

可参见章节查看aclrtMemcpy的详细说明。

#### 函数原型

```
aclError sanitizerRtMemcpy(void *dst, size_t destMax, const void *src, size_t count, aclrtMemcpyKind kind, char const *filename, int lineno);
```

#### 参数说明
**表1**参数说明
参数名

输入/输出

描述

dst

输入

目的内存地址指针。

destMax

输入

目的内存地址的最大内存长度，单位为Byte。

src

输入

源内存地址指针。

count

输入

内存复制的长度，单位为Byte。

kind

输入

预留参数，系统内部会根据源内存地址指针、目的内存地址指针判断是否可以将源地址的数据复制到目的地址，如果不可以，则系统会返回报错。

filename

输入

内存复制被调用处的文件名。

lineno

输入

内存复制被调用处的行号。
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