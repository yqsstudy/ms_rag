---
title: "同步检测"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0181.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0181.html"
---

# 同步检测

在Ascend C算子开发过程中，必须成对使用SetFlag和WaitFlag，同步检测功能用于找出算子中未配对的SetFlag指令。

若存在多余SetFlag指令，不会直接导致当前算子的竞争问题，却会改变硬件计数器的状态，进而可能导致后续算子的同步指令配对错误。若这些后续算子本身不存在竞争，竞争检测也不会报错，但前序算子的计数器变化可能导致实际竞争情况的发生，通过同步检测功能，能够有效识别前序算子中的多余SetFlag指令问题，避免后续算子受影响。

- [同步检测单独启用时不会执行内存检测和竞争检测，因此建议用户先使用内存检测](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/83RC1alpha001/devaids/optool/atlasopdev_16_0042.html)[和竞争检测](atlasopdev_16_0043.html#ZH-CN_TOPIC_0000002504880738)，若竞争检测无异常报告，但算子存在竞争现象时，再考虑使用同步检测对前序算子进行检查。
- 若存在多余WaitFlag指令，将会导致当前算子的后续指令被阻塞，从而出现算子运行停滞的现象。此时，开发者无需工具提示，便可自行发现问题。

#### 支持的同步异常类型
**表1**同步异常类型
异常名

描述

位置

同步检测

算子中存在未配对的SetFlag同步指令时，虽然对当前算子的功能没有直接影响，却会引发计数器状态错误。可能会扰乱后续算子的同步指令配对，进而影响后续算子的计算精度。

Kernel
|  |  |  |
| --- | --- | --- |
|  |  |  |

#### 启用同步检测
**运行msSanitizer工具时，执行如下命令，启用同步检测功能（synccheck）。****
```
mssanitizer --tool=synccheck application   // application为用户程序
```

- *启动工具后，将会在当前目录下自动生成工具运行日志文件mssanitizer_{TIMESTAMP}**_{PID*}.log。
- 当用户程序运行完成后，界面将会打印异常报告，异常的具体含义请参见同步异常报告解析。

#### 同步异常报告解析

同步检测异常报告会依次列出每个算子中未配对的SetFlag指令的相关信息，包括源流水和目标流水以及具体位置。

```
1
2
3
4
5
6
7
```

```
====== WARNING: Unpaired set_flag instructions detected  // 提示检出未配对的set_flag指令
======    from PIPE_S to PIPE_MTE3 in kernel  // 标识从PIPE_S到PIPE_MTE3的同步，PIPE_MTE3等待PIPE_S
======    in block aiv(0) on device 1  // 异常代码对应Vector核的block索引和设备号，此处为0核1卡
======    code in pc current 0x2c94 (serialNo:31) // 当前异常发生的pc指针和调用api行为的序列号
======    #0 /home/Ascend/compiler/tikcpp/tikcfw/impl/kernel_event.h:785:13  // 以下为异常发生代码的调用栈，包含文件名、行号和列号
======    #1 /home/Ascend/compiler/tikcpp/tikcfw/interface/kernel_common.h:150:5
======    #2 /home/test/ascendc_test_syncall/kernel.cpp:26:9

```
|  |  |
| --- | --- |
**父主题：**[异常检测（msSanitizer）](atlasopdev_16_0038.html)