---
title: "工具概述"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0062.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0062.html"
---

# 工具概述

[msDebug是一款面向昇腾设备的算子调试工具，用于调试NPU侧运行的算子程序，为算子开发人员提供调试手段。调试手段包括了读取昇腾设备内存与寄存器、暂停与恢复程序运行状态等。用户使用其他拉起算子的方式或msOpST工具](atlasopdev_16_0028.html#ZH-CN_TOPIC_0000002504880724)在真实的硬件环境中对算子的功能进行测试后，可根据实际测试情况选择是否使用msDebug工具进行功能调试。

- [若要使能msDebug工具](atlasopdev_16_0061.html#ZH-CN_TOPIC_0000002505040594)，需通过以下两种方法安装NPU驱动固件（CANN 8.1.RC1之后的版本且驱动为25.0.RC1之后的版本，推荐使用方法一）：
  - **方法一：驱动安装时指定--full**参数，然后再使用root用户执行echo 1 > /proc/debug_switch命令打开调试通道，msDebug工具便可正常使用。
```
./Ascend-hdk-<chip_type>-npu-driver_<version>_linux-<arch>.run --full
```

  - **方法二：驱动安装时指定--debug**[参数，具体安装操作请参见安装NPU驱动和固件](https://www.hiascend.com/document/detail/zh/canncommercial/850/softwareinst/instg/instg_0005.html?Mode=PmIns&InstallType=local&OS=openEuler)。
```
./Ascend-hdk-<chip_type>-npu-driver_<version>_linux-<arch>.run --debug
```

- 调试通道权限较大，存在安全风险，请谨慎使用，生产环境不推荐使用，使用本调试工具即代表认可并接受该风险。

#### 功能特性

msDebug工具支持调试所有的昇腾算子，包含Ascend C算子（Vector、Cube以及Mix融合算子）程序，用户可根据实际情况进行选择，具体请参见表1。
**表1**msDebug工具功能介绍
功能

链接

断点设置

[断点设置](atlasopdev_16_0066.html#ZH-CN_TOPIC_0000002505040600)

打印变量和内存

[内存与变量打印](atlasopdev_16_0067.html#ZH-CN_TOPIC_0000002536800563)

单步调试

[单步调试](atlasopdev_16_0068.html#ZH-CN_TOPIC_0000002536920535)

中断运行

[中断运行](atlasopdev_16_0069.html#ZH-CN_TOPIC_0000002504880776)

核切换

[核切换](atlasopdev_16_0070.html#ZH-CN_TOPIC_0000002505040604)

检查程序状态

[读取寄存器](atlasopdev_16_0071.html#ZH-CN_TOPIC_0000002536800567)

调试信息展示

[调试信息展示](atlasopdev_16_0072.html#ZH-CN_TOPIC_0000002536920541)

解析Core dump文件

[解析异常算子dump文件](atlasopdev_16_0149.html#ZH-CN_TOPIC_0000002504880784)
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

- [通过键盘输入“CTRL+C”后，算子执行将会被停止，工具会根据当前已有信息生成性能数据文件](atlasopdev_16_0092.html#ZH-CN_TOPIC_0000002536800599)。若不需要生成该文件，可再次键盘输入“CTRL+C”指令。
- 若未指定--output参数，默认保存为当前工具执行的路径，需确保群组和其他组的用户不具备当前路径的上一级目录的写入权限。

#### 命令汇总

- *用户需自行保证可执行文件或用户程序（application*）执行的安全性。
  - *建议限制对可执行文件或用户程序（application*）的操作权限，避免提权风险。
  - 不建议进行高危操作（删除文件、删除目录、修改密码及提权命令等），避免安全风险。

- 通过键入help命令可查看msDebug工具支持的所有命令。表2[之外的命令属于开源调试器lldb实现，使用需注意相关风险，详细使用方法可参考lldb官方文档https://lldb.llvm.org/](https://lldb.llvm.org/)。
**表2**命令参考说明
命令

命令缩写

描述

示例

*breakpoint set -f filename -**l**linenum*

b

*增加断点，f**ilename**为算子实现代码文件*.cpp，linenum*为代码文件对应的具体行号。

```
b add_custom.cpp:85
```

run

r

运行程序。

```
r
```

continue

c

继续运行。

```
c
```

*print variable*

p

打印变量。

```
p zLocal
```

*frame variable*

var

显示当前作用域内的所有局部变量。

```
var
```

memory read

x

读内存。

```
x -m GM -f float16[] 0x00001240c0037000 -c 2 -s 128
```

- -m：指定内存位置，支持GM/UB/L0A/L0B/L0C/L1/FB/STACK/DCACHE/ICACHE 说明：
[STACK/DCACHE/ICACHE仅在解析异常算子dump文件](atlasopdev_16_0149.html#ZH-CN_TOPIC_0000002504880784)时使用。

- -s：指定每行打印字节数
- -c：指定打印的行数
- -f：指定打印的数据类型
- *0x00001240c0037000*：需要读取的内存地址，请根据实际环境进行替换

ascend info devices

-

查询Device信息。

```
ascend info devices
```

ascend info cores

-

查询算子所运行的aicore相关信息。

```
ascend info cores
```

ascend info tasks

-

查询算子所运行的task相关信息。

```
ascend info tasks
```

ascend info stream

-

查询算子所运行的stream相关信息。

```
ascend info stream
```

ascend info blocks

-

查询算子所运行的block相关信息。
打印所运行的blocks相关信息：
```
ascend info blocks 
```
打印所运行的blocks在当前中断处的代码：
```
ascend info blocks -d
```

*ascend aic id*

-

切换调试器所聚焦的Cube核。

```
ascend aic 1
```

*ascend aiv id*

-

切换调试器所聚焦的Vector核。

```
ascend aiv 5
```

“CTRL+C”

-

手动中断算子运行程序并回显中断位置信息。

通过键盘输入。

register read

re r

读取寄存器值；-a读取所有寄存器值；$REG_NAME读取指定名称的寄存器值；

```
register read -a
re r $PC
```

thread step-over

next或n

在同一个调用栈中，移动到下一个可执行的代码行。

```
n
```

thread step-in

step或s

使用step in命令可进入到函数内部进行调试。

```
s
```

thread step-out

finish

使用finish命令会执行完函数内剩余部分，并返回主程序继续执行。

```
finish
```

thread backtrace

bt

用于展示此时代码调用栈信息。
说明：
- bt命令当前只适用于coredump特性场景，调用栈信息仅在stop_reason为以下error时：CUBE_ERROR、CCU_ERROR、MTE_ERROR、VEC_ERROR、FIXP_ERROR，保证准确性。
- [如果展示的函数名过长，可以参考Link](https://lldb.llvm.org/use/formatting.html)进行设置：
```
setting set frame-format "frame #${frame.index}: ${frame.pc}{ ${module.file.basename}{{${frame.no-debug}${function.pc-offset}}}}{ at ${line.file.basename}:${line.number}{:${line.column}}}{${function.is-optimized} [opt]}{${frame.is-artificial} [artificial]}\n"
```

```
bt
```

target modules add <kernel.o>

image add [kernel.o]

用于PyTorch框架调用算子时，导入算子调试信息。
说明：
当程序执行run命令后，需先执行image add命令导入调试信息。然后再执行image load命令使导入的调试信息生效。
**
```
image add xx.o       
```

target modules load --file <kernel.o> --slide <address>

image load -f <kernel.o> -s <address>

用于PyTorch框架调用算子时，加载算子调试信息，使导入的调试信息生效。
**
```
image load -f xx.o -s 0
```

msdebug --core corefile [kernel.o|fatbin]

-

- 用于加载Core dump文件。
- 第二个参数可选，需要输入-g编译的kernel.o或者fatbin格式的可执行二进制文件的路径，用于展示代码行调用栈。

```
msdebug --core corefile xx.o
msdebug --core corefile
```

ascend info summary

-

用于查看Core dump文件信息。

```
ascend info summary
```

*help msdebug_command*

-

输出对应工具命令的帮助信息。打印信息将会展示该命令的功能描述、使用语法以及参数选项。

```
help run
```
**核切换**命令的帮助信息如下所示：****
```
(msdebug) help ascend aic
change the id of the focused ascend aicore.
Syntax: ascend aic <id>
```
**ascend info blocks**命令的帮助信息如下所示：****
```
(msdebug) help ascend info blocks
show blocks overall info.
Syntax: ascend info blocks
Command Options Usage:
  ascend info blocks [-d]
       -d ( --details )
            Show stopped states for all blocks.
```
|  |  |  |  |
| --- | --- | --- | --- |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |

#### 调用场景
支持如下调用算子的场景：
- Kernel直调算子开发：Kernel直调。
[Kernel直调的场景，详细信息可参考Kernel直调。具体操作请参见上板调试Vector算子](atlasopdev_16_0074.html#ZH-CN_TOPIC_0000002536800571)。

- 工程化算子开发：单算子API调用。
[单算子API调用的场景，详细信息可参考单算子API调用。具体操作请参见调用Ascend CL单算子](atlasopdev_16_0075.html#ZH-CN_TOPIC_0000002536920545)。

- AI框架算子适配：PyTorch框架。
[通过PyTorch框架进行单算子调用的场景，详细信息可参考基于OpPlugin算子适配开发](https://www.hiascend.com/document/detail/zh/Pytorch/600/modthirdparty/modparts/thirdpart_0012.html)[具体操作请参见调试PyTorch接口调用的算子](atlasopdev_16_0076.html#ZH-CN_TOPIC_0000002504880790)。

#### 补充说明

msDebug工具还提供了以下扩展程序，具体请参考表3。
**表3**扩展程序说明
程序名称

说明

msdebug-mi（msDebug Machine Interface）

提供机机交互接口用于实现数据解析，用户无需关注。
|  |  |
| --- | --- |
|  |  |
**父主题：**[算子调试（msDebug）](atlasopdev_16_0061.html)