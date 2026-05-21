---
title: "sanitizerReportMalloc"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0059.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0059.html"
---

# sanitizerReportMalloc

#### 功能说明

手动上报GM内存分配信息。

#### 函数原型

```
void sanitizerReportMalloc(void *ptr, uint64_t size);
```

此接口是__sanitizer_report_malloc接口的封装， __sanitizer_report_malloc接口为弱函数，只有当用户程序被检测工具拉起时才会生效。

#### 参数说明
**表1**参数说明
参数名

输入/输出

描述

ptr

输入

分配的内存地址。

size

输入

分配的内存长度。
|  |  |  |
| --- | --- | --- |
|  |  |  |
|  |  |  |

#### 返回值

无

#### 调用示例

无
**父主题：**[sanitizer接口](atlasopdev_16_0141.html)