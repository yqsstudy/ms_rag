---
title: "工具使用"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_00851.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_00851.html"
---

# 工具使用

msProf工具包含msprof op和msprof op simulator两种使用方式，协助用户定位算子内存、算子代码以及算子指令的异常，实现全方位的算子调优。两种使用方式的详细说明请参考表1。
**表1**msprof op和msprof op simulator功能说明表
功能名称

适用场景

使用方式

展示的图形

msprof op

适用于实际运行环境中的性能分析，可协助用户定位算子内存和性能瓶颈。

直接分析运行中的算子，无需额外配置，适合在板环境中快速定位算子性能问题。

[计算内存热力图](atlasopdev_16_0086.html#ZH-CN_TOPIC_0000002504880804)

[Roofline瓶颈分析图](atlasopdev_16_0119.html#ZH-CN_TOPIC_0000002505040630)

[Cache热力图](atlasopdev_16_0158.html#ZH-CN_TOPIC_0000002536800589)

[通算流水图](atlasopdev_16_0139.html#ZH-CN_TOPIC_0000002536920563)

[算子代码热点图](atlasopdev_16_0088.html#ZH-CN_TOPIC_0000002504880812)
说明：
[若要实现Cache热力图跳转](atlasopdev_16_0158.html#ZH-CN_TOPIC_0000002536800589__zh-cn_topic_0000002502746412_li14516202184314)[功能，需参考msprof op配置](atlasopdev_16_0083.html#ZH-CN_TOPIC_0000002536800585__zh-cn_topic_0000002534506431_section9922438155112)进行配置。

msprof op simulator

适用于开发和调试阶段，进行详细仿真调优，可协助用户分析算子指令和代码热点问题。

[需要参考msprof op simulator配置](atlasopdev_16_0083.html#ZH-CN_TOPIC_0000002536800585__zh-cn_topic_0000002534506431_section15215201620113)，配置环境变量（如LD_LIBRARY_PATH）和编译选项（如添加-g生成调试信息），适合在仿真环境中详细分析算子行为。

[指令流水图](atlasopdev_16_0087.html#ZH-CN_TOPIC_0000002504880808)

[算子代码热点图](atlasopdev_16_0088.html#ZH-CN_TOPIC_0000002504880812)

[内存通路吞吐率波形图](atlasopdev_16_0160.html#ZH-CN_TOPIC_0000002505040638)
说明：
资料中的msprof op simulator的仿真结果仅供参考，算子真实的运行情况以用户的实际仿真数据为准。
|  |  |  |  |
| --- | --- | --- | --- |
|  |  |  |  |
|  |  |  |  |

- msProf工具的使用依赖CANN包中的msopprof可执行文件，该文件中的接口使用和msprof op一致，该文件为CANN包自带，无需单独安装。
- 不支持在同一个Device侧同时拉起多个性能采集任务。
- 使用msprof op和msprof op simulator之前，用户需保证app功能正常。

#### msprof op

1. *登录运行环境，使用msprof op 可选参数*[app [arguments]格式开启算子上板调优，可选参数的具体情况请参考表2](atlasopdev_16_0082.html#ZH-CN_TOPIC_0000002505040624__zh-cn_topic_0000002534506413_table17624248171315)。具体命令示例如下：
********************
```
msprof op --output=$HOME/projects/output $HOME/projects/MyApp/out/main    // --output为可选参数  $HOME/projects/MyApp/out/main为使用的app 
```

2. 通过以下两种方式执行算子调优：

  - 基于可执行文件，
    - *单算子场景，以add_custom_npu*为例。示例一：**
```
msprof op ./add_custom_npu
```
示例二：******
```
msprof op --aic-metrics=<select_metrics> --output=./output_data ./add_custom_npu 
```

    - 多算子场景。若test中有Add，MatlMul，Sub算子，可配合--launch-count和--kernel-name使用，可以指定采集Add和Sub算子。******
```
msprof op --launch-count=10 --kernel-name="Add|Sub" --output=./output_data ./test  // ./test为用户二进制文件，需放置在命令末尾
```

  - **基于输入算子二进制文件*.o**[的配置文件.json，具体请参见json配置文件说明](atlasopdev_16_0104.html#ZH-CN_TOPIC_0000002536920583)。********
```
msprof op --config=./add_test.json --aic-metrics=<select_metrics> --output=./output_data
```

3. *命令完成后，会在默认路径或指定的“--output”目录下生成以“OPPROF_{timestamp}**_XXX*”命名的文件夹，在“--aic-metrics”全部开启时，结构示例如下：

  - 采集多卡多算子的场景。
对多卡并行的通算融合算子（MC2或LCCL算子）进行调优时，结果目录下会存在若干以Device ID为名的子目录，这取决于定义时指定的NPU数量，每个NPU的调优结果会分别存放在对应的Device ID目录下。

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
```

```
└──OPPROF_{timestamp}_XXX
├── device0                  // 运行时使用昇腾AI处理器的ID
└── device1                
  ├── OpName0                // OpName0为采集算子名称
  │ ├── 0                   // 表示算子调度顺序
  │ │ ├──dump              // 与单算子含义一致，存放过程件的文件夹
   │ │ └──xxx_yyy.csv       // xxx代表该算子生成的指标种类名,例如L2Cache,具体指标种类可参考中的csv文件介绍,yyy为csv文件的时序后缀,例如L2Cache_20240603022812284.csv
  │ │ └──visualize_data.bin 
  ├── OpName1               
  │ ├── 0
  │ │ ├──dump 
  │ │ └──xxx_yyy.csv
  │ │ └──visualize_data.bin 
   ├── OpName2         
  │ ├── 0
  │ │ ├── dump  
  │ │ └── xxx_yyy.csv
  │ │ └──visualize_data.bin 
  │ │ └── trace.json      // 此文件仅适用于MC2和LCCL类型通算融合算子  

```
|  |  |
| --- | --- |

  - 采集单卡多算子场景。
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
```

```
└──OPPROF_{timestamp}_XXX
├── OpName0                  // OpName0为采集算子名称
│ ├── 0                     // 表示算子调度顺序
│ │ ├── dump                // 与单算子含义一致，存放过程件的文件夹
│ │ └── xxx_yyy.csv   // xxx代表该算子生成的指标种类名,例如L2Cache,具体指标种类可参考中的csv文件介绍,yyy为csv文件的时序后缀,例如L2Cache_20240603022812284.csv
│ │ └──visualize_data.bin 
│ ├── 1
│ │ ├──dump 
│ │ └──xxx_yyy.csv
│ │ └──visualize_data.bin 
├── OpName1         
│ ├── 0
│ │ ├── dump  
│ │ └── xxx_yyy.csv
│ │ └── visualize_data.bin 

```
|  |  |
| --- | --- |

  - 采集单卡单算子场景。
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
```

```
OPPROF_{timestamp}_XXX
├── dump
├── ArithmeticUtilization.csv
├── L2Cache.csv
├── Memory.csv
├── MemoryL0.csv
├── MemoryUB.csv
├── OpBasicInfo.csv
├── PipeUtilization.csv
├── ResourceConflictRatio.csv
├── visualize_data.bin 

```
|  |  |
| --- | --- |

**表2**msprof op文件介绍
名称

说明

dump文件夹

原始的性能数据，用户无需关注。

ArithmeticUtilization.csv

[Cube和Vector类型的指令耗时和占比，可参考ArithmeticUtilization（Cube及Vector类型指令耗时和占比）](atlasopdev_16_0093.html#ZH-CN_TOPIC_0000002504880818)。

L2Cache.csv

[L2 Cache命中率，可参考L2Cache（L2 Cache命中率）](atlasopdev_16_0094.html#ZH-CN_TOPIC_0000002505040642)。

Memory.csv

[UB/L1/L2/主存储器采集内存读写带宽速率，可参考Memory（内存读写带宽速率）](atlasopdev_16_0095.html#ZH-CN_TOPIC_0000002536800603)。

MemoryL0.csv

[L0A/L0B/L0C采集内存读写带宽速率，可参考MemoryL0（L0读写带宽速率）](atlasopdev_16_0096.html#ZH-CN_TOPIC_0000002536920577)。

MemoryUB.csv

[mte/vector/scalar采集ub读写带宽速率，可参考MemoryUB（UB读写带宽速率）](atlasopdev_16_0097.html#ZH-CN_TOPIC_0000002504880822)。

PipeUtilization.csv

[采集计算单元和搬运单元耗时和占比，可参考PipeUtilization（计算单元和搬运单元耗时占比）](atlasopdev_16_0099.html#ZH-CN_TOPIC_0000002536800607)。

ResourceConflictRatio.csv

[UB上的bank group、bank conflict和资源冲突在所有指令中的占比，可参考ResourceConflictRatio（资源冲突占比）](atlasopdev_16_0100.html#ZH-CN_TOPIC_0000002536920579)。

OpBasicInfo.csv

[算子基础信息，包含算子名称、block dim和耗时等信息，可参考OpBasicInfo（算子基础信息）](atlasopdev_16_0098.html#ZH-CN_TOPIC_0000002505040646)。

visualize_data.bin

[算子基础信息、计算单元负载、热点函数和Roofline瓶颈分析等信息的可视化呈现文件，具体请参考计算内存热力图](atlasopdev_16_0086.html#ZH-CN_TOPIC_0000002504880804)[、Roofline瓶颈分析图](atlasopdev_16_0119.html#ZH-CN_TOPIC_0000002505040630)[、Cache热力图](atlasopdev_16_0158.html#ZH-CN_TOPIC_0000002536800589)[、通算流水图](atlasopdev_16_0139.html#ZH-CN_TOPIC_0000002536920563)[和算子代码热点图](atlasopdev_16_0088.html#ZH-CN_TOPIC_0000002504880812)。
说明：
  - [visualize_data.bin可通过MindStudio Insight工具进行可视化展示，具体使用方法请参考《MindStudio Insight工具用户指南](https://www.hiascend.com/document/detail/zh/mindstudio/830/GUI_baseddevelopmenttool/msascendinsightug/Insight_userguide_0002.html)》。
  - msprof op的热点函数功能仅支持Atlas A2 训练系列产品/Atlas A2 推理系列产品。
  - [当前，仅支持生成MC2和LCCL类型通算融合算子的通算流水图](atlasopdev_16_0139.html#ZH-CN_TOPIC_0000002536920563)。
  - [MC2和LCCL类型通算融合算子不支持生成Cache热力图](atlasopdev_16_0158.html#ZH-CN_TOPIC_0000002536800589)[和算子代码热点图](atlasopdev_16_0088.html#ZH-CN_TOPIC_0000002504880812)，且不支持Atlas 推理系列产品。
  - 单位GB/s表示每秒传输1GB的数据量。

trace.json

[通算流水可视化呈现文件，Chrome浏览器具体请参考通算流水图](atlasopdev_16_0139.html#ZH-CN_TOPIC_0000002536920563)。
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
|  |  |
|  |  |

4. [将visualize_data.bin文件导入MindStudio Insight后，将会展示计算内存热力图](atlasopdev_16_0086.html#ZH-CN_TOPIC_0000002504880804)[、Roofline瓶颈分析图](atlasopdev_16_0119.html#ZH-CN_TOPIC_0000002505040630)[、Cache热力图](atlasopdev_16_0158.html#ZH-CN_TOPIC_0000002536800589)[、通算流水图](atlasopdev_16_0139.html#ZH-CN_TOPIC_0000002536920563)[和算子代码热点图](atlasopdev_16_0088.html#ZH-CN_TOPIC_0000002504880812)。
5. [将trace.json文件导入Chrome浏览器或MindStudio Insight后，将会展示通算流水图](atlasopdev_16_0139.html#ZH-CN_TOPIC_0000002536920563)。

#### msprof op simulator

算子调优工具支持仿真环境下的性能数据采集和自动解析。

- 仿真环境不支持采集MC2和HCCL类型的算子。
- 用户设置的仿真核数不能超过物理核数。
- [若用户仅需关注部分算子性能时，可在Atlas A3 训练系列产品/Atlas A3 推理系列产品、Atlas 推理系列产品和Atlas A2 训练系列产品/Atlas A2 推理系列产品的单核内调用TRACE_START](https://www.hiascend.com/document/detail/zh/canncommercial/850/API/ascendcopapi/atlasascendc_api_07_1212.html)[和TRACE_STOP](https://www.hiascend.com/document/detail/zh/canncommercial/850/API/ascendcopapi/atlasascendc_api_07_1213.html)接口。并在编译配置文件中添加-DASCENDC_TRACE_ON，具体操作请参见添加-DASCENDC_TRACE_ON的方法[。然后，才能生成该范围内的流水图信息，具体流水图显示内容可参考指令流水图](atlasopdev_16_0087.html#ZH-CN_TOPIC_0000002504880808)。
- 用户需在编译配置文件中添加-DASCENDC_TRACE_ON，具体修改方法可参考以下样例工程。[AddKernelInvocationNeo算子工程](https://gitee.com/ascend/samples/tree/master/operator/ascendc/0_introduction/3_add_kernellaunch/AddKernelInvocationNeo/cmake)，需在${git_clone_path}/samples/operator/ascendc/0_introduction/3_add_kernellaunch/AddKernelInvocationNeo/cmake/npu_lib.cmake文件中新增以下代码。************************
```
ascendc_compile_definitions
(
    ...
    -DASCENDC_TRACE_ON
)
```

1. [登录运行环境，需要使用msprof op simulator开启算子仿真调优，并配合使用仿真可选参数和用户待调优程序（app [arguments]）进行调优，仿真可选参数请参考表3](atlasopdev_16_0082.html#ZH-CN_TOPIC_0000002505040624__zh-cn_topic_0000002534506413_table1811793417333)。算子仿真调优可以通过以下两种方式执行：

  - 基于可执行文件。
    - *单算子场景，以add_custom_npu*为例。
```
msprof op simulator --soc-version=Ascendxxxyy --output=./output_data ./add_custom_npu // xxxyy为用户实际使用的具体芯片类型
```

    - 多算子场景。若test中有Add，MatlMul，Sub算子，可配合--launch-count和--kernel-name使用，可以指定采集Add和Sub算子。******
```
msprof op simulator --soc-version=Ascendxxxyy --launch-count=10 --kernel-name="Add|Sub" --output=./output_data ./test  // xxxyy为用户实际使用的具体芯片类型，./test需要放置在命令末尾
```

  - **基于输入算子二进制文件*.o**的配置文件.json。
--config场景下，仅支持使用LD_LIBRARY_PATH导入环境变量，不支持使用--soc-version参数。
**********
```
export LD_LIBRARY_PATH=${INSTALL_DIR}/tools/simulator/Ascendxxxyy/lib:$LD_LIBRARY_PATH  // xxxyy为用户实际使用的具体芯片类型
msprof op simulator --config=./add_test.json --output=./output_data
```

2. *命令完成后，会在指定的“--output”目录下生成以“OPPROF_{timestamp}**_XXX*”命名的文件夹，结构示例如下：

  - 采集单个算子场景。
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
```

```
OPPROF_{timestamp}_XXX
├── dump
└── simulator
    ├── core0.veccore0       // 按照core*.veccore*或core*.cubecore*目录存放各核的数据文件
    │   ├── core0.veccore0_code_exe.csv
    │   ├── core0.veccore0_instr_exe.csv
    │   └── trace.json     // 该核的仿真指令流水图文件
    ├── core0.veccore1
    │   ├── core0.veccore1_code_exe.csv
    │   ├── core0.veccore1_instr_exe.csv
    │   └── trace.json
    ├── core1.veccore0
    │   ├── core1.veccore0_code_exe.csv
    │   ├── core1.veccore0_instr_exe.csv
    │   └── trace.json
    ├── ... 
    ├── visualize_data.bin 
    └── trace.json      // 全部核的仿真指令流水图文件

```
|  |  |
| --- | --- |

  - 采集多个算子场景。
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
```

```
└──OPPROF_{timestamp}_XXX
├── OpName1           // OpName1为采集算子名称
│ ├── 0              // 表示算子调度到的顺序
│ │ ├── dump        // 与单算子含义一致，存放过程件的文件夹
│ │ └──simulator    // 与单算子simulator文件夹内容一致,但simulator文件夹中的csv文件均会增加时序后缀,例如core*_code_exe_20240429111143146.csv
│ ├── 1
│ │ ├── dump        
│ │ └──simulator
│ ├── dump          // 存放过程件的文件夹
├── OpName2         
│ ├── 0
│ │ ├── dump       
│ │ └── simulator
│ ├── dump  

```
|  |  |
| --- | --- |

**表3**msprof op simulator文件介绍
名称

说明

dump文件夹

原始仿真生成的dump数据存放文件夹。

simulator文件夹
说明：
dump数据文件分析结果存放文件夹。

core*_code_exe.csv

[代码行耗时，*代表0~n核，以便用户快速确定编写的代码中最耗时的部分，可参考代码行耗时数据文件](atlasopdev_16_0101.html#ZH-CN_TOPIC_0000002505040652)。

core*_instr_exe.csv

[代码指令详细信息，*代表0~n核，以便用户快速确定最耗时的指令，可参考代码指令信息文件](atlasopdev_16_0102.html#ZH-CN_TOPIC_0000002536800609)。

visualize_data.bin

[仿真流水图和仿真热点函数等信息可视化呈现文件，具体请参见指令流水图](atlasopdev_16_0087.html#ZH-CN_TOPIC_0000002504880808)[、算子代码热点图](atlasopdev_16_0088.html#ZH-CN_TOPIC_0000002504880812)[和内存通路吞吐率波形图](atlasopdev_16_0160.html#ZH-CN_TOPIC_0000002505040638)。
说明：
[生成仿真流水图以及仿真热点函数等信息可视化呈现文件visualize_data.bin，该文件可通过MindStudio Insight工具进行可视化展示，具体使用方法请参考《MindStudio Insight工具用户指南](https://www.hiascend.com/document/detail/zh/mindstudio/830/GUI_baseddevelopmenttool/msascendinsightug/Insight_userguide_0002.html)》。

trace.json

[仿真指令流水图文件，包括每个核的子文件以及全部核的汇总文件，可参考指令流水图](atlasopdev_16_0087.html#ZH-CN_TOPIC_0000002504880808)[和内存通路吞吐率波形图](atlasopdev_16_0160.html#ZH-CN_TOPIC_0000002505040638)。
|  |  |  |
| --- | --- | --- |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |

3. **可选：**[将visualize_data.bin文件导入MindStudio Insight后，将会展示指令流水图](atlasopdev_16_0087.html#ZH-CN_TOPIC_0000002504880808)[、算子代码热点图](atlasopdev_16_0088.html#ZH-CN_TOPIC_0000002504880812)[和内存通路吞吐率波形图](atlasopdev_16_0160.html#ZH-CN_TOPIC_0000002505040638)。
4. [将trace.json文件导入Chrome浏览器或MindStudio Insight后，将会展示指令流水图](atlasopdev_16_0087.html#ZH-CN_TOPIC_0000002504880808)[和内存通路吞吐率波形图](atlasopdev_16_0160.html#ZH-CN_TOPIC_0000002505040638)。
**父主题：**[算子调优（msProf）](atlasopdev_16_0081.html)