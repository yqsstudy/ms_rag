---
title: "未初始化检测"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0128.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0128.html"
---

# 未初始化检测

未初始化检测功能是一种重要的内存安全保护机制，旨在识别并防止由于使用未初始化的变量而导致的内存异常。

#### 支持的未初始化异常类型
**表1**未初始化异常类型
异常名

描述

位置

支持地址空间

未初始化

内存申请后为未初始化状态，未对内存进行写入，直接读取未初始化的值导致的异常。

Kernel、Host

GM、UB、L1、L0{ABC}、栈空间
|  |  |  |  |
| --- | --- | --- | --- |
|  |  |  |  |

#### 启用未初始化检测
**运行msSanitizer工具时，执行如下命令，启用未初始化检测功能（initcheck）。****
```
mssanitizer --tool=initcheck application   // application为用户程序
```

- *启动工具后，将会在当前目录下自动生成工具运行日志文件mssanitizer_{TIMESTAMP}**_{PID*}.log。
- 当用户程序运行完成后，界面将会打印异常报告，异常的具体含义请参见未初始化异常报告解析。
- 由于硬件限制，某些指令仅支持以Block形式进行数据搬运。当参与计算的实际数据量不是Block大小的整数倍时，可能会不可避免地带入部分无效数据（即“脏数据”），这可能导致工具报告初始化异常，用户需自行判断这些“脏数据”是否会影响计算结果。

#### 未初始化异常报告解析

未初始化检测异常报告会输出多种不同类型的异常信息，以下将对一些简单的异常信息示例进行说明，帮助用户解读异常报告中的信息。

未初始化的异常场景一般是算子读取了已申请但未初始化的内存，发生在GM、UB、L1、L0{ABC}、栈空间上。

```
1
2
3
4
5
6
7
8
```

```
====== ERROR: uninitialized read of size 224  // 异常的基本信息，包含读取的未初始化字节数
======    at 0x12c0c0015000 on GM in add_custom_kernel  // 异常发生的内存位置信息，包含发生的核函数名、地址空间与内存地址，此处的内存地址指一次内存访问中的首地址
======    in block aiv(0) on device 0  // 异常代码对应Vector核的block索引
======    code in pc current 0x77c (serialNo:10) // 当前异常发生的pc指针和调用api行为的序列号
======    #0 ${ASCEND_HOME_PATH}/compiler/tikcpp/tikcfw/impl/dav_c220/kernel_operator_data_copy_impl.h:58:9  // 以下为异常发生代码的调用栈，包含文件名、行号和列号
======    #1 ${ASCEND_HOME_PATH}/compiler/tikcpp/tikcfw/inner_interface/inner_kernel_operator_data_copy_intf.cppm:58:9
======    #2 ${ASCEND_HOME_PATH}/compiler/tikcpp/tikcfw/inner_interface/inner_kernel_operator_data_copy_intf.cppm:443:5
======    #3 uninitialized_read/add_custom.cpp:18:5

```
|  |  |
| --- | --- |
**父主题：**[异常检测（msSanitizer）](atlasopdev_16_0038.html)