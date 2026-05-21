---
title: "调试信息展示"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0072.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0072.html"
---

# 调试信息展示

#### ascend info devices
输入以下命令查询算子运行的设备信息，*所在行代表当前聚焦的设备。
```
1
2
3
```

```
(msdebug) ascend info devices
  Device Aic_Num Aiv_Num Aic_Mask Aiv_Mask
*    1      1       2      0x10000     0x3

```
|  |  |
| --- | --- |

通算融合算子场景将会显示多个Device ID。
关键信息说明如下表：**表1**信息说明
字段

释义

Device

设备逻辑ID。

Aic_Num

使用的Cube核数量。

Aiv_Num

使用的Vector核数量。

Aic_Mask

实际使用的Cube的mask码，用64 bit位表示，如果第n位bit为1，表示使用了Cube n。

Aiv_Mask

实际使用的Vector的mask码，用64 bit位表示，如果第n位bit为1，表示使用了Vector n。
|  |  |
| --- | --- |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |

#### ascend info cores
输入以下命令查询算子运行的核信息，*所在行代表当前聚焦的核。如下所示当前聚焦的核为aiv的“core 0”。
```
1
2
3
4
5
```

```
(msdebug) ascend info cores
  CoreId  Type  Device Stream Task Block         PC               stop reason
   16     aic      1     3     0     0     0x12c0c00f1fc0         breakpoint 1.1
*   0     aiv      1     3     0     0     0x12c0c00f8fcc         breakpoint 1.1
    1     aiv      1     3     0     0     0x12c0c00f8d3c         breakpoint 1.1

```
|  |  |
| --- | --- |
关键信息说明如下表：**表2**信息说明
字段

释义

CoreId

aiv或aic的核id，从0开始。

Type

核类型，包括aic或aiv。

Device

设备逻辑id。

Stream

当前Kernel函数下发的Stream ID，Stream由一系列的task组成。

Task

当前Stream里的Task ID。Task表示下发给Task scheduler处理的任务。

Block

表示核函数将会在几个核上执行。每个执行该核函数的核会被分配一个逻辑ID，即block_id。

PC

当前核上的PC逻辑绝对地址。

Stop Reason

表示程序执行停止原因，有breakpoint、step in、 step over和ctrl+c等。
|  |  |
| --- | --- |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |

#### ascend info tasks
输入以下命令查询算子运行的Task信息，*所在行代表当前聚焦的Task，包括Device ID、Stream ID、Task ID、Invocation（被调用的核函数名称）。
```
1
2
3
```

```
(msdebug) ascend info tasks
  Device Stream Task Invocation
*   1       3     0  matmul_leakyrelu_custom

```
|  |  |
| --- | --- |

#### ascend info stream
输入以下命令查询算子运行的Stream信息，*所在行代表当前聚焦的Stream，包括Device ID、Stream ID、Type（核类型，包括aic或aiv）。
```
1
2
3
```

```
(msdebug) ascend info stream
  Device Stream Type
*   1      3    aiv

```
|  |  |
| --- | --- |

#### ascend info blocks
输入以下命令查询算子运行的Block信息，*所在行代表当前聚焦的Block，包括Device ID、Stream ID、Task ID、Block ID。
```
1
2
3
4
5
```

```
(msdebug) ascend info blocks
  Device Stream Task Block
    1      3     0     0
*   1      3     0     0
    1      3     0     0

```
|  |  |
| --- | --- |

输入以下命令，打印所运行的Block在当前中断处的代码。

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
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
```

```
(msdebug) ascend info blocks -d
Current stop state of all blocks:
 
[CoreId 16, Block 0]
* thread #1, name = 'matmul_leakyrelu', stop reason = breakpoint 1.1
    frame #0: 0x0000000000008fc0 device_debugdata`_ZN7AscendC14KfcMsgGetStateEj_mix_aic(flag=0) at kfc_comm.h:188
   185      return static_cast<KFC_Enum>((flag & 0xffff0000) >> KFC_MSG_BYTE_OFFSET);
   186  }
   187  __aicore__ inline uint32_t KfcMsgGetState(uint32_t flag)
-> 188  {
   189      return (flag & 0x00008000);
   190  }
   191  __aicore__ inline uint32_t KfcMsgMakeFlag(KFC_Enum funID, uint16_t instID)
 
[* CoreId 0, Block 0]
* thread #1, name = 'matmul_leakyrelu', stop reason = breakpoint 1.1
    frame #0: 0x000000000000ffcc device_debugdata`_ZN17MatmulLeakyKernelIDhDhffE7CopyOutEj_mix_aiv(this=0x0000000000167b60, count=0) at matmul_leakyrelu_kernel.cpp:116:1
   113          (uint16_t)((tiling.N - tiling.baseN) * sizeof(cType) / DEFAULT_C0_SIZE)};
   114      DataCopy(cGlobal[startOffset], reluOutLocal, copyParam);
   115      reluOutQueue_.FreeTensor(reluOutLocal);
-> 116  }
   117
   118  template <typename aType, typename bType, typename cType, typename biasType>
   119  __aicore__ inline void MatmulLeakyKernel<aType, bType, cType, biasType>::CalcOffset(int32_t blockIdx,
 
[CoreId 1, Block 0]
* thread #1, name = 'matmul_leakyrelu', stop reason = breakpoint 1.1
    frame #0: 0x000000000000fd3c device_debugdata`_ZN7AscendC13WaitEventImplEt_mix_aiv(flagId=1) at kernel_operator_sync_impl.h:142:5
   139
   140  __aicore__ inline void WaitEventImpl(uint16_t flagId)
   141  {
-> 142      wait_flag_dev(flagId);
   143  }
   144
   145  __aicore__ inline void SetSyncBaseAddrImpl(uint64_t config)

```
|  |  |
| --- | --- |
**父主题：**[算子调试（msDebug）](atlasopdev_16_0061.html)