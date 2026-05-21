---
title: "sanitizerReportFree"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0060.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0060.html"
---

# sanitizerReportFree

#### 功能说明

手动上报GM内存释放信息。

#### 函数原型

```
void sanitizerReportFree(void *ptr);
```

此接口是__sanitizer_report_free接口的封装，__sanitizer_report_free接口为弱函数，只有当用户程序被检测工具拉起时才会生效。

#### 参数说明
**表1**参数说明
参数名

输入/输出

描述

ptr

输入

释放的内存地址。
|  |  |  |
| --- | --- | --- |
|  |  |  |

#### 返回值

无

#### 调用示例

无
**父主题：**[sanitizer接口](atlasopdev_16_0141.html)