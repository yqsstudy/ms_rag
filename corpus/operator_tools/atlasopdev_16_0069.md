---
title: "中断运行"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0069.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0069.html"
---

# 中断运行

1. Host侧或Device侧的算子运行程序卡顿时，用户可通过键盘输入“CTRL+C”，可手动中断算子运行程序并回显中断位置信息。
若运行程序出现卡顿的现象，可以通过键盘输入“CTRL+C”中断运行程序。运行卡顿的原因可能是以下情况：
  - 用户程序本身存在死循环，需要通过修复程序解决。
  - 算子使用了同步类指令。

```
 1
 2
 3
 4
 5
 6
 7
 8
 9
10
11
12
13
14
15
16
```

```
(msdebug) r
Process 173221 launched: '${INSTALL_DIR}/projects/mix/matmul_leakyrelu.fatbin' (aarch64)
[Launch of Kernel matmul_leakyrelu_custom on Device 1]
//  键盘输入CTRL+C命令
Process 173221 stopped
[Switching to focus on Kernel matmul_leakyrelu_custom, CoreId 35, Type aiv]
* thread #1, name = 'matmul_leakyrelu', stop reason = signal SIGSTOP
    frame #0: 0x000000000000ef5c device_debugdata`_ZN17MatmulLeakyKernelIDhDhffE10CalcOffsetEiiRK11TCubeTilingRiS4_S4_S4__mix_aiv(this=<unavailable>, blockIdx=<unavailable>, usedCoreNum=<unavailable>, tiling=<unavailable>, offsetA=<unavailable>, offsetB=<unavailable>, offsetC=<unavailable>, offsetBias=<unavailable>) at matmul_leakyrelu_kernel.cpp:127:5
   124      auto mCoreIndx = blockIdx % mSingleBlocks;
   125      auto nCoreIndx = blockIdx / mSingleBlocks;
   126
-> 127      while(true) {
   128      }
   129      offsetA = mCoreIndx * tiling.Ka * tiling.singleCoreM;
   130      offsetB = nCoreIndx * tiling.singleCoreN;
(msdebug)

```
|  |  |
| --- | --- |

2. 调试完以后，执行q命令并输入Y或y结束调试。

```
1
2
```

```
(msdebug) q
Quitting LLDB will kill one or more processes. Do you really want to proceed: [Y/n] y

```
|  |  |
| --- | --- |


- 此功能仅支持调试在msDebug工具内启动的算子程序，无法调试在msDebug工具外启动的应用程序。
- [中断生效后，支持调试信息展示](atlasopdev_16_0072.html#ZH-CN_TOPIC_0000002536920541)[和核切换](atlasopdev_16_0070.html#ZH-CN_TOPIC_0000002505040604)[功能，暂不支持单步调试](atlasopdev_16_0068.html#ZH-CN_TOPIC_0000002536920535)[，读取寄存器](atlasopdev_16_0071.html#ZH-CN_TOPIC_0000002536800567)[、内存与变量打印](atlasopdev_16_0067.html#ZH-CN_TOPIC_0000002536800563)和continue命令。
**父主题：**[算子调试（msDebug）](atlasopdev_16_0061.html)