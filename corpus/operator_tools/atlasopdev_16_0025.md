---
title: "查看算子仿真流水图"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0025.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0025.html"
---

# 查看算子仿真流水图

msOpGen工具通过解析用户生成的dump文件，并生成算子仿真流水图文件（trace.json）。

1. [参考Link](https://gitee.com/ascend/samples/tree/master/operator/ascendc/0_introduction/1_add_frameworklaunch)，在${git_clone_path}/samples/operator/ascendc/0_introduction/1_add_frameworklaunch路径下运行install.sh文件，并生成CustomOp文件夹。


此样例工程不支持
 Atlas A3 训练系列产品
 和
 Atlas 训练系列产品
 。
****
```
./install.sh -v Ascendxxxyy   # xxxyy为用户实际使用的具体芯片类型
```

2. 编译算子工程。

  1. [参考编译前准备](atlasopdev_16_0024.html#ZH-CN_TOPIC_0000002504880720__zh-cn_topic_0000002502586626_section4684858183614)章节，完成编译相关配置。
  2. 在算子工程目录CustomOp下，执行如下命令，进行算子工程编译。
若要生成算子仿真流水图，需要将当前目录下CMakePresets.json文件中CMAKE_BUILD_TYPE修改为“Debug”。
编译完成后，将会在build_out目录生成.run算子包。****
```
./build.sh
```

3. 在自定义算子包所在路径下，执行如下命令，部署算子包。

********
```
./build_out/custom_opp_<target_os>_<target_architecture>.run
```

4. 切换到AclNNInvocation仓的目录${git_clone_path}/samples/operator/ascendc/0_introduction/1_add_frameworklaunch/AclNNInvocation，执行以下命令。

```
./run.sh
```

5. [使能环境变量后，请参考msprof op simulator](atlasopdev_16_00851.html#ZH-CN_TOPIC_0000002536920559__zh-cn_topic_0000002534426389_section8684154219309)功能进行仿真，并生成dump数据。

```
export LD_LIBRARY_PATH=${git_clone_path}/samples/operator/ascendc/0_introduction/1_add_frameworklaunch/CustomOp/build_out/op_host/:$LD_LIBRARY_PATH
```

6. 生成算子仿真流水图文件。

执行如下命令，参数说明请参见表1。
**********
```
msopgen sim -c core{id} -d xx/{path of dump data} -subc {sub core id} -out {output path} -reloc {path of .o file or executable file} 
```
**表1**参数说明
参数名称

参数描述

是否必选

sim

用于性能仿真相关操作。
说明：
[msopgen sim命令将于MindStudio下个版本下线，下线后您可使用msOpProf提供的仿真能力，具体信息请参见工具使用](atlasopdev_16_00851.html#ZH-CN_TOPIC_0000002536920559)。

是

-c，--core-id

核编号。

配置处理器号，如：core0。

是

-d，--dump-dir

dump文件所在路径，可配置为绝对路径或者相对路径。

是

-subc，--subcore_id

子核编号，支持展示单个子核。

*dump文件名带有veccore{id}**或cubecore{id}**时，需配置此参数指定待解析的dump文件。如文件名为core0**.veccore0*.instr_log.dump，“veccore0”即为subcore id。

二选一
说明：
仅
 Atlas A3 训练系列产品
 /
 Atlas A3 推理系列产品
 和
 Atlas A2 训练系列产品
 /
 Atlas A2 推理系列产品
 需配置该参数。

-mix，--mixcore-mode

支持展示Mix融合算子。

-reloc，--relocatable-file

**配置为Kernel侧算子编译后生成的.o**文件或可执行文件所在路径。

**进行流水图与代码行的映射，并生成代码行和指令耗时.csv**文件。
说明：
**基于算子工程编译生成包含调试信息的.o**[文件（路径为${git_clone_path}/samples/operator/ascendc/0_introduction/1_add_frameworklaunch/CustomOp/build_out/op_kernel/binary/ascendxxxy/add_custom/AddCustom_*.o），即需要修改CMakePresets.json中CMAKE_BUILD_TYPE为“Debug”，具体可参考编译操作](atlasopdev_16_0024.html#ZH-CN_TOPIC_0000002504880720__zh-cn_topic_0000002502586626_zh-cn_topic_0000001691887130_section122481539171817)。

否

-out，--output

输出文件的路径，可配置为绝对路径或者相对路径，并且工具执行用户具有可读写权限。

是

-h，--help

输出帮助信息。

否
|  |  |  |
| --- | --- | --- |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |

执行以下命令。
示例一：**********
```
msopgen sim -c core0 -d xx/{model}/ca/add_custom/add_custom_pre_static_add_custom -out ./output_data -subc cubecore0 -reloc xx/.o
```

  - -c：指定待解析dump文件的core id，如：core0。
  - *-d：指定性能仿真环境下生成的dump文件所在路径。例如："{model}**/ca/add_custom*/add_custom_pre_static_add_custom"。
  - *-subc：指定待解析dump文件的subcore id，如文件名为core0.cubecore0*.instr_log.dump，“cubecore0”即为subcore id。（仅
 Atlas A3 训练系列产品
 /
 Atlas A3 推理系列产品
 和
 Atlas A2 训练系列产品
 /
 Atlas A2 推理系列产品
 需配置该参数）
  - -reloc：指定Kernel侧算子编译生成的.o文件或可执行文件所在路径。
示例二：**
```
msopgen sim -c core0 -d xx/{model}/ca/add_custom/add_custom_pre_static_add_custom -out ./output_data -mix
```

  - -c：指定待解析dump文件的core id，如：core0。
  - *-d：指定性能仿真环境下生成的dump文件所在路径。例如："{model}**/ca/add_custom*/add_custom_pre_static_add_custom"。
  - -mix ：配置此参数表示支持展示Mix融合算子。

7. 查看算子仿真流水图文件。

**可以在Chrome浏览器中输入“chrome://tracing”地址，将输出路径下的dump2trace_core*.json**文件拖到空白处打开，通过键盘上的快捷键（W：放大，S：缩小，A：左移，D：右移）进行查看，如下图所示。
**图1**
![](figure/zh-cn_image_0000002502746518.png "点击放大")**单个子核展示
 
 
 
 图2**
![](figure/zh-cn_image_0000002534506553.png "点击放大")Mix融合算子展示**表2**字段说明
字段名

字段含义

VECTOR

向量运算单元。

SCALAR

标量运算单元。

CUBE

矩阵乘运算单元。

MTE1

数据搬运流水，数据搬运方向为：L1 ->{L0A/L0B, UBUF}。

MTE2

数据搬运流水，数据搬运方向为：{DDR/GM, L2} ->{L1, L0A/B, UBUF}。

MTE3

数据搬运流水，数据搬运方向为：UBUF -> {DDR/GM, L2, L1}。

FIXP

数据搬运流水，数据搬运方向为：FIXPIPE L0C -> OUT/L1。（仅
 Atlas A3 训练系列产品
 /
 Atlas A3 推理系列产品
 和
 Atlas A2 训练系列产品
 /
 Atlas A2 推理系列产品
 支持展示）

FLOWCTRL

控制流指令。

ICmiss

未命中ICache。
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
|  |  |

8. 查看代码行或指令耗时文件。

*在输出路径下打开代码行耗时文件{核编号}**_***code_exe_prof.csv，如下图所示。
 
 图3**
![](figure/zh-cn_image_0000002502586704.png "点击放大")*代码行耗时文件
 
 
 
 
 在输出路径下打开指令耗时文件{核编号}_***instr_exe_prof.csv，如下图所示。
 
 图4**
![](figure/zh-cn_image_0000002534426519.png "点击放大")指令耗时文件
通过文件中的“call count”及“cycles”字段可以分别查看代码行或指令的调用次数和累计耗时。

**父主题：**[算子工程创建（msOpGen）](atlasopdev_16_0017.html)