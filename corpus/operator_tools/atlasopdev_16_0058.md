---
title: "sanitizerRtMemcpy2dAsync"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0058.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0058.html"
---

# sanitizerRtMemcpy2dAsync

#### 功能说明

调用aclrtMemcpy2dAsync接口完成矩阵数据内存复制，并向检测工具上报内存复制信息。此接口为异步接口。实际的矩阵数据内存复制行为和参数含义与aclrtMemcpy2dAsync一致。

可参见章节查看aclrtMemcpy2dAsync的详细说明。

#### 函数原型

```
aclError sanitizerRtMemcpy2dAsync(void *dst, size_t dpitch, const void *src, size_t spitch, size_t width, size_t height, aclrtMemcpyKind kind, aclrtStream stream, char const *filename, int lineno);
```

#### 参数说明
**表1**参数说明
参数名

输入/输出

描述

dst

输入

目的内存地址指针。

dpitch

输入

目的内存中相邻两列向量的地址距离。

src

输入

源内存地址指针。

spitch

输入

源内存中相邻两列向量的地址距离。

width

输入

待复制的矩阵宽度。

height

输入

待复制的矩阵高度。

height最大设置为5*1024*1024=5242880，否则接口返回失败。

kind

输入

内存复制的类型。

stream

输入

当前矩阵数据内存复制行为指定的stream。

filename

输入

矩阵数据内存复制被调用处的文件名。

lineno

输入

矩阵数据内存复制被调用处的行号。
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

#### 返回值

返回0表示成功，返回其它值表示失败。

#### 调用示例

[具体操作请参见使用示例的步骤4](atlasopdev_16_0047.html#ZH-CN_TOPIC_0000002505040574__zh-cn_topic_0000002502746432_zh-cn_topic_0000001748761501_li1423525185711)。
**父主题：**[sanitizer接口](atlasopdev_16_0141.html)