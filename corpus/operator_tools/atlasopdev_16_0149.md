---
title: "解析异常算子dump文件"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0149.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0149.html"
---

# 解析异常算子dump文件

客户现场发生硬件异常时，需要反复压测复现问题，定位效率低。为了解决该问题，系统检测到潜在的硬件异常时，会自动触发一个dump操作，捕获当前的状态信息。msDebug工具通过对异常算子dump文件的解析，即使在没有主动压测的情况下也能收集到足够的数据用于问题分析。通过上述功能，不仅提高了硬件异常问题的定位效率，还减少因反复压测给用户带来的不便。

#### 操作步骤

1. 准备acl.json配置文件。

  - [工程化算子开发：单算子API调用](atlasopdev_16_0062.html#ZH-CN_TOPIC_0000002536800557__zh-cn_topic_0000002502586550_zh-cn_topic_0000001831604757_li679913151018)[场景：参考《应用开发指南 (C&C++)](https://www.hiascend.com/document/detail/zh/canncommercial/850/appdevg/acldevg/aclcppdevg_000000.html)[》的“ 初始化与去初始化](https://www.hiascend.com/document/detail/zh/canncommercial/850/appdevg/acldevg/aclcppdevg_000007.html)”节点，自行创建acl.json文件，然后通过aclinit接口进行加载。
  - [AI框架算子适配：PyTorch框架](atlasopdev_16_0062.html#ZH-CN_TOPIC_0000002536800557__zh-cn_topic_0000002502586550_zh-cn_topic_0000001831604757_li32921336161911)场景：在用户torch_npu的安装目录中搜索acl.json文件。

配置acl.json文件后将不能使用msDebug的其他功能。

2. [参见《应用开发指南 (C&C++)](https://www.hiascend.com/document/detail/zh/canncommercial/850/appdevg/acldevg/aclcppdevg_000000.html)[》的“aclInit](https://www.hiascend.com/document/detail/zh/canncommercial/850/API/appdevgapi/aclcppdevg_03_0022.html)”章节的配置文件示例（异常算子Dump配置），开启生成异常算子dump文件的功能。

  1. 在acl.json配置文件中，将dump_scene参数设置为aic_err_detail_dump。
  2. 在acl.json配置文件中，配置dump_path参数设置导出异常算子dump文件的路径。

3. 程序崩溃时（如内存溢出、段错误等），触发生成异常算子core文件，文件名以.core结尾。
4. 使用msDebug工具执行以下命令，加载异常算子dump文件。

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
msdebug --core output2/extra-info/data-dump/0/xxx.core add.fatbin
msdebug(MindStudio Debugger) is part of MindStudio Operator-dev Tools.
The tool provides developers with a mechanism for debugging Ascend kernels running on actual hardware.
This enables developers to debug Ascend kernels without being affected by potential changes brought by simulation and emulation environments.
(msdebug) target create "add.fatbin" --core "output2/extra-info/data-dump/0/xxx.core"
Core file '/home/xxx/coredump_test/output2/extra-info/data-dump/0/xxx.core' (aarch64) was loaded.
[Switching to focus on CoreId 26, Type aiv]

```
|  |  |
| --- | --- |

如果需要查看调用栈，需使用-O2/O3 + -g选项编译生成包含调试信息的kernel.o文件，或者生成fatbin结构的ELF文件。

原因：在算子执行过程中，若因指令执行导致硬件异常，硬件通常会继续执行若干条指令后再上报异常并生成core文件。因此，core文件中的内存和寄存器数据可能并不准确。不过，PC寄存器的值通常会被修正。在O2/O3优化下默认inline，不需要栈内存数据，仍可以回溯准确的调用栈；而在O0优化下会强制no inline，且栈内存数据不准确，通常只有0栈帧是准确的。

5. 查看异常算子dump文件信息。

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
51
52
53
54
55
56
57
58
59
60
```

```
msdebug --core output2/extra-info/data-dump/0/xxx.core /home/xxxxx/Ascend/cann/opp/vendors/customize/op_impl/ai_core/tbe/kernel/ascend910b/add_custom/AddCustom_xxxx.o

msdebug(MindStudio Debugger) is part of MindStudio Operator-dev Tools.
The tool provides developers with a mechanism for debugging Ascend kernels running on actual hardware.
This enables developers to debug Ascend kernels without being affected by potential changes brought by simulation and emulation environments.
(msdebug) target create "/home/xxx/Ascend/cann/opp/vendors/customize/op_impl/ai_core/tbe/kernel/ascend910b/add_custom/AddCustom_xxx.o" --core "output2/extra-info/data-dump/0/xxx.core"
Core file '/home/xxx/output2
/extra-info/data-dump/0/xxx.core' (hiipu64) was loaded.
[Switching to focus on CoreId 34, Type aiv]

(msdebug) ascend info summary
  CoreId  CoreType        PC         DeviceId    ChipType
    33       AIV    0x12c0412004c8       0        A2/A3
 *  34       AIV    0x12c0412007c0       0        A2/A3
    35       AIV    0x12c0412007c0       0        A2/A3
    36       AIV    0x12c0412007c0       0        A2/A3
    37       AIV    0x12c0412007c0       0        A2/A3
    38       AIV    0x12c0412007c0       0        A2/A3
    39       AIV    0x12c0412007c0       0        A2/A3
    40       AIV    0x12c0412007c0       0        A2/A3

  Id           DataType                   MemType                     Addr                       Size             CoreId    CoreType    Dim
   0    DEVICE_KERNEL_OBJECT                GM                   0x12c041200000                 167872             NA         AIV        NA
   1            STACK                    GM/DCACHE           0xff000108000(invalid)              32768             33         AIV        NA
   2            STACK                    GM/DCACHE           0xff000110000(invalid)              32768             34         AIV        NA
   3            STACK                    GM/DCACHE           0xff000118000(invalid)              32768             35         AIV        NA
   4            STACK                    GM/DCACHE           0xff000120000(invalid)              32768             36         AIV        NA
   5            STACK                    GM/DCACHE           0xff000128000(invalid)              32768             37         AIV        NA
   6            STACK                    GM/DCACHE           0xff000130000(invalid)              32768             38         AIV        NA
   7            STACK                    GM/DCACHE           0xff000138000(invalid)              32768             39         AIV        NA
   8            STACK                    GM/DCACHE           0xff000140000(invalid)              32768             40         AIV        NA
   9      WORKSPACE_TENSOR                  GM                         0x0                         0               NA          NA        NA
  10         TILING_DATA                 GM/DCACHE               0x12c100000038                   16               NA          NA        NA
  11        OUTPUT_TENSOR                   GM                   0x12c0c0024000                  32768             NA          NA        [8, 2048]
  12        INPUT_TENSOR                    GM                   0x12c0c0012000                  32768             NA          NA        [8, 2048]
  13        INPUT_TENSOR                    GM                   0x12c0c001b000                  32768             NA          NA        [8, 2048]
  14            ARGS                     GM/DCACHE               0x12c100000000                   96               NA          NA        NA

(msdebug) bt
   * thread #1, stop reason = VEC_ERROR
     * frame #0: 0x000012c0412004c8 AddCustom_xxx.o`::AddCustom_xxx_0(uint8_t *__gm__, uint8_t *__gm__, uint8_t *__gm__, u
   int8_t *__gm__, uint8_t *__gm__) [inlined] void AscendC::TPipe::ReleaseEventID<(AscendC::HardEvent)5>(this=<unavailable>, id=<unavailable>) at kernel_tpipe_impl.h:454:24
       frame #1: 0x000012c0412004c8 AddCustom_xxx.o`::AddCustom_xxx_0(uint8_t *__gm__, uint8_t *__gm__, uint8_t *__gm__, u
   int8_t *__gm__, uint8_t *__gm__) [inlined] AscendC::TQueBind<(AscendC::TPosition)0, (AscendC::TPosition)9, 2, 0>::AllocBuffer(this=<unavailable>) at kernel_tquebind_impl.h:512:3
   6
       frame #2: 0x000012c041200474 AddCustom_xxx.o`::AddCustom_xxx_0(uint8_t *__gm__, uint8_t *__gm__, uint8_t *__gm__, u
   int8_t *__gm__, uint8_t *__gm__) [inlined] AscendC::LocalTensor<half> AscendC::TQueBind<(this=<unavailable>)0, (AscendC::TPosition)9, 2, 0>::AllocTensor<half>() at kernel_tquebi
   nd_impl.h:78:16
       frame #3: 0x000012c041200474 AddCustom_xxx.o`::AddCustom_xxx_0(uint8_t *__gm__, uint8_t *__gm__, uint8_t *__gm__, u
   int8_t *__gm__, uint8_t *__gm__) [inlined] KernelAdd::CopyIn(this=<unavailable>, progress=<unavailable>) at add_custom.cpp:42:57
       frame #4: 0x000012c041200474 AddCustom_xxx.o`::AddCustom_xxx_0(uint8_t *__gm__, uint8_t *__gm__, uint8_t *__gm__, u
   int8_t *__gm__, uint8_t *__gm__) at add_custom.cpp:33:13
       frame #5: 0x000012c04120039c AddCustom_xxx.o`::AddCustom_xxx_0(uint8_t *__gm__, uint8_t *__gm__, uint8_t *__gm__, u
   int8_t *__gm__, uint8_t *__gm__) [inlined] add_custom_0_tilingkey(x=<unavailable>, y=<unavailable>, z=<unavailable>, workspace=<unavailable>, tiling=<unavailable>) at add_custom
   .cpp:83:8
       frame #6: 0x000012c041200064 AddCustom_xxx.o`::AddCustom_xxx_0(uint8_t *__gm__, uint8_t *__gm__, uint8_t *__gm__, u
   int8_t *__gm__, uint8_t *__gm__) [inlined] ascendc_auto_gen_add_custom_kernel(x_in__=<unavailable>, y_in__=<unavailable>, z_out_=<unavailable>, workspace=<unavailable>, tiling=<
   unavailable>) at AddCustom_xxx_3800102_kernel.cpp:43:5
       frame #7: 0x000012c04120004c AddCustom_xxx.o`::AddCustom_xxx_0(x_in__=<unavailable>, y_in__=<unavailable>, z_out_=<
   unavailable>, workspace=<unavailable>, tiling=<unavailable>) at AddCustom_xxx_3800102_kernel.cpp:48:5

```
|  |  |
| --- | --- |

6. [请参考核切换](atlasopdev_16_0070.html#ZH-CN_TOPIC_0000002505040604)[、读取寄存器](atlasopdev_16_0071.html#ZH-CN_TOPIC_0000002536800567)[以及内存与变量打印](atlasopdev_16_0067.html#ZH-CN_TOPIC_0000002536800563)章节的内存打印相关操作定位硬件异常。
7. 调试完以后，执行q命令并输入Y或y结束调试。

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

**父主题：**[算子调试（msDebug）](atlasopdev_16_0061.html)