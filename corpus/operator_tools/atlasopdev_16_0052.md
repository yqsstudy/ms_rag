---
title: "sanitizerRtFree"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0052.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0052.html"
---

# sanitizerRtFree

#### 功能说明

调用aclrtFree接口释放Device上的内存，并向检测工具上报内存释放信息。实际的内存释放行为和参数含义与aclrtFree一致。

可参见章节查看aclrtFree的详细说明。

#### 函数原型

```
aclError sanitizerRtFree(void *devPtr, char const *filename, int lineno);
```

#### 参数说明
**表1**参数说明
参数名

输入/输出

描述

devPtr

输入

待释放内存的指针。

filename

输入

内存释放被调用处的文件名。

lineno

输入

内存释放被调用处的行号。
|  |  |  |
| --- | --- | --- |
|  |  |  |
|  |  |  |
|  |  |  |

#### 返回值

返回0表示成功，返回其它值表示失败。

#### 调用示例

[具体操作请参见使用示例的步骤4](atlasopdev_16_0047.html#ZH-CN_TOPIC_0000002505040574__zh-cn_topic_0000002502746432_zh-cn_topic_0000001748761501_li1423525185711)。
**父主题：**[sanitizer接口](atlasopdev_16_0141.html)