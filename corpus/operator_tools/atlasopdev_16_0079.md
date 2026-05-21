---
title: "msDebug工具打印Tensor变量功能不可用，提示“unavailable”或“memory read failed”"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0079.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0079.html"
---

# msDebug工具打印Tensor变量功能不可用，提示“unavailable”或“memory read failed”

#### 现象描述

提示“unavailable”或“Failed to dereference pointer from xxx for DW_OP_deref: memory read failed for xxx”。

#### 原因分析

单步调试功能不支持Tensor按值传递的写法。

#### 解决措施

当打印对象a为Tensor类型且以值传递作为函数入参时会出现该问题。
****
```
void Foo(const LocalTensor<float> a); // 该写法变量a打印失败
```

若需打印该变量，可修改代码使对象a以引用传递作为函数入参，修复该问题。
********
```
void Foo(const LocalTensor<float> &a); // 该写法变量a可正常打印
```
**父主题：**[FAQ](atlasopdev_16_0077.html)