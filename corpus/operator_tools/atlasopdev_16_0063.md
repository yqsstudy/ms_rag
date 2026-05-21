---
title: "使用前准备"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0063.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0063.html"
---

# 使用前准备

#### 环境准备

[请参考环境准备](atlasopdev_16_0003.html#ZH-CN_TOPIC_0000002536800441)，完成相关环境变量的配置。

#### 使用约束

- [若要使能msDebug工具需要安装驱动，具体安装方法请参考工具概述](atlasopdev_16_0062.html#ZH-CN_TOPIC_0000002536800557)。
- 单Device仅支持使用单个msDebug工具进行调试，且不推荐同时运行其他算子程序。
- 当被调试程序调用多个算子时，msDebug工具仅支持对指定的单个算子进行调试。
- 调试算子时，溢出检测功能会关闭。

#### 导入调试信息

[算子调试前，需先启用调试-g -O0编译选项重新编译，使算子二进制带上调试信息，具体方法可参考基于样例工程编译算子](atlasopdev_16_0074.html#ZH-CN_TOPIC_0000002536800571__zh-cn_topic_0000002534426429_zh-cn_topic_0000001795016076_li339451095417)。

[在-O0编译选项场景下，算子程序的行为与-O2编译场景会不一致。因此算子内部的竞争问题不建议在-O0编译选项下定位，推荐使用msSanitizer工具的竞争检测](atlasopdev_16_0043.html#ZH-CN_TOPIC_0000002504880738)功能进行定位。
**通常情况下，算子调试信息会自动被导入msDebug工具。但算子二进制以.o**[文件形式独立存在并部署的情况下（例如通过Ascend CL单算子调用的场景](atlasopdev_16_0075.html#ZH-CN_TOPIC_0000002536920545)），需要选择如下方法导入算子调试信息：
- 多算子场景时，仅支持导入指定单算子的调试信息，不支持导入多算子的调试信息，且仅支持对指定单算子的.o文件进行调试。
- [复杂的算子编译会生成多个.o文件，如何选择具体的.o文件导入请参见算子使用"-O0 -g"编译选项编译后，运行出错，"min stack size is xxx, larger than current process default size 32768. Please modify aclInit json, and reboot process."](atlasopdev_16_0145.html)。

- 方法一：在调试前，配置如下环境变量，指定算子加载路径，导入调试信息。********
```
export LAUNCH_KERNEL_PATH={path_to_kernel}/my_kernel.o  //{path_to_kernel}为Kernel侧.o文件所在目录
```

- 方法二：在执行run命令前，执行image add命令，指定算子加载路径，导入调试信息。******
```
(msdebug) image add {path_to_kernel}/my_kernel.o   //{path_to_kernel}为Kernel侧.o文件所在目录
```

  - image add仅适用于PyTorch场景的导入方式。
  - 若需要程序运行后导入调试信息，还需执行image load命令完成算子调试信息的加载。**
```
(msdebug) image load -f {path_to_kernel}/my_kernel.o -s 0 
```

#### 启动工具

msDebug工具支持以下两种启动方式：
**若工具弹出Cannot read termcap database; using dumb terminal settings.***的提示信息，可以通过配置export TERMINFO=xx**消除提示，xx*为本地TERMINFO路径：**
```
export TERMINFO=xx    //xx信息可通过infocmp -D命令查询，可以选择符合当前终端配置的路径作为TERMINFO值
```

- *加载可执行文件application*。
  1. *算子编译后可获取NPU侧可执行文件application*。
*基于Ascend C算子的Kernel侧框架执行一键式编译运行，可生成NPU侧可执行文件application*，具体操作可参考Kernel直调。

  2. 输入如下命令，使用msDebug工具加载可执行文件。**********
```
$ msdebug ./application
```
若可执行文件有其他入参，则按照如下形式传入入参：**
```
msdebug -- ./application --flag1 arg1 --flag2 args2 ...
```

- 加载调用算子的Python脚本
  1. *完成了PyTorch框架的适配插件开发后，即可实现从PyTorch框架调用Ascend C自定义算子，可以通过自定义Python脚本test_ops_custom.py*调用算子。
[通过PyTorch框架进行单算子调用的场景，详细信息可参考基于OpPlugin算子适配开发](https://www.hiascend.com/document/detail/zh/Pytorch/600/modthirdparty/modparts/thirdpart_0012.html)。

  2. 输入如下命令，使用msDebug工具加载Python脚本。
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
$ msdebug python3 test_ops_custom.py
msdebug(MindStudio Debugger) is part of MindStudio Operator-dev Tools.
The tool provides developers with a mechanism for debugging Ascend kernels running on actual hardware.
This enables developers to debug Ascend kernels without being affected by potential changes brought by simulation and emulation environments.
(msdebug) target create "python3"
Current executable set to '${INSTALL_DIR}/projects/application' (aarch64).
(msdebug) settings set -- target.run-args  "test_ops_custom.py"
(msdebug)

```
|  |  |
| --- | --- |

#### 调试退出
输入以下命令，退出调试器。****
```
(msdebug) q
[localhost add_ascendc_sample]$ 
```

该调试通道无法单独关闭，若要关闭调试通道，需要通过覆盖安装方式，具体请参见对应的NPU驱动和固件安装文档。
**父主题：**[算子调试（msDebug）](atlasopdev_16_0061.html)