---
title: "读取寄存器"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0071.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0071.html"
---

# 读取寄存器

当用户使用msDebug调起算子后，可以通过命令行读取当前断点所在设备的寄存器值。具体介绍如下：

- 输入register read -a后，返回当前设备上所有可用的寄存器值。
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
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
```

```
(msdebug) register read -a
                  PC = 0x12C0C00F1F88
                COND = 0x0
                CTRL = 0x100000000003C
                GPR0 = 0x12C041200100
                GPR1 = 0x146FD9
                GPR2 = 0x146FC8
                GPR3 = 0x8001000800
                GPR4 = 0x80300000100
                GPR5 = 0x80000000000
                GPR6 = 0x0
                GPR7 = 0x300000000
                GPR8 = 0x3
                GPR9 = 0x1000000
               GPR10 = 0xFFF
               GPR11 = 0xFC0
               GPR12 = 0x0
               GPR13 = 0x0
               GPR14 = 0x0
               GPR15 = 0x11
               GPR16 = 0x7FFF
               GPR17 = 0x7A0
               GPR18 = 0x0
               GPR19 = 0x0
               GPR20 = 0x0
               GPR21 = 0x0
               GPR22 = 0x0
               GPR23 = 0x0
               GPR24 = 0x0
               GPR25 = 0x0
               GPR26 = 0x0
               GPR27 = 0x0
               GPR28 = 0x0
               GPR29 = 0x146EE8
               GPR30 = 0x147640
               GPR31 = 0x12C0C00F1ED4
               LPCNT = 0x0
              STATUS = 0x0
             SYS_CNT = 0x774E308602
       ICACHE_PRL_ST = 0x0
       SAFETY_CRC_EN = 0x0
       ST_ATOMIC_CFG = 0x5
      CALL_DEPTH_CNT = 0x5
      CONDITION_FLAG = 0x1
      FFTS_BASE_ADDR = 0xE7FFE044F000
    CUBE_EVENT_TABLE = 0x70000000000
    FIXP_EVENT_TABLE = 0x0
    MTE1_EVENT_TABLE = 0x700000000
    MTE2_EVENT_TABLE = 0x0
  SCALAR_EVENT_TABLE = 0x0

```
|  |  |
| --- | --- |

- 输入register read ${变量名}，返回当前设备上该寄存器值。一次性读取多个寄存器时，需用空格隔开。
  - 当变量名在当前设备上可用时，返回该寄存器值。
  - **当变量名在当前设备上不可用时，返回Invalid register name****'**变量名'。

```
1
2
3
4
```

```
(msdebug) register read $PC $test $GPR30
                  PC = 0x12C0C00F1F88
Invalid register name 'test'.
               GPR30 = 0x147640

```
|  |  |
| --- | --- |

**父主题：**[算子调试（msDebug）](atlasopdev_16_0061.html)