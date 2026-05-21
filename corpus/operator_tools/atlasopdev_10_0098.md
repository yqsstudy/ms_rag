---
title: "生成/执行测试用例"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_10_0098.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_10_0098.html"
---

# 生成/执行测试用例

指导用户根据算子测试用例定义文件生成ST测试数据及测试用例执行代码，在硬件环境上执行算子测试用例。

#### 开发环境与运行环境合设场景

1. [请参见环境准备](atlasopdev_16_0003.html#ZH-CN_TOPIC_0000002536800441)，配置CANN软件所需基本环境变量。
2. ST测试用例执行时，会使用AscendCL接口加载单算子模型文件并执行，所以需要配置AscendCL应用编译所需其他环境变量，如下所示。
**
```
export DDK_PATH=${INSTALL_DIR}
export NPU_HOST_LIB=${INSTALL_DIR}/{arch-os}/devlib
```

  - ${INSTALL_DIR}请替换为CANN软件安装后文件存储路径。以root用户安装为例，则安装后文件存储路径为：/usr/local/Ascend/cann。
  - *{arch-os}中**arch**表示操作系统架构，os*表示操作系统。

3. 执行如下命令生成/执行测试用例。
************
```
msopst run -i {*.json}  -soc {soc version}  -out {output path} -c {case name} -d {device id} -conf {msopst.ini path} -err_thr "[threshold1,threshold2]"
```
**表1**参数说明
参数名称

参数描述

是否必选

run

用于执行算子的ST测试用例。

是

-i，--input

算子测试用例定义文件（*.json）的路径，可配置为绝对路径或者相对路径。

**此处的json文件为执行msopst create**[命令后的输出，算子测试用例定义文件的详细说明请参见表2](atlasopdev_10_0097.html#ZH-CN_TOPIC_0000002505040678__zh-cn_topic_0000002534426431_table103623575476)。

是

-soc, --soc_version

配置为昇腾AI处理器的类型。
说明：
*如果无法确定具体的<soc_version>***，则在安装昇腾AI处理器的服务器执行npu-smi info***命令进行查询，在查询到的“Name”前增加Ascend信息，例如“Name”对应取值为xxxyy**，实际配置的<soc_version>**值为Ascendxxxyy*。

是

-out，--output

生成文件所在路径，可配置为绝对路径或者相对路径，并且工具执行用户具有可读写权限。若不配置该参数，则默认生成在执行命令的当前路径。

否

-c，--case_name

  - 配置为需要执行的case的名字，若需要同时运行多个case，多个case之间使用逗号分隔。
  - 若配置为“all”，或者不配置此参数，代表执行所有case。

否

-d，--device_id

NPU设备ID，设置运行ST测试用例的昇腾AI处理器的ID。

若未设置此参数，默认为：0。

否

-err_thr，--error_threshold

配置自定义精度标准，取值为含两个元素的列表："[threshold1，threshold2]"

  - threshold1：算子输出结果与标杆数据误差阈值，若误差大于该值则记为误差数据。
  - threshold2：误差数据在全部数据占比阈值。若误差数据在全部数据占比小于该值，则精度达标，否则精度不达标。

默认值为："[0.01,0.05]"。

取值范围为："[0.0,1.0]"。
说明：
  - 配置的列表需加引号以避免一些问题。例如配置为：-err_thr "[0.01,0.05]"。
  - 若测试用例json文件和执行msopst命令时均配置该参数，以执行msopst命令时配置的精度标准进行比对。若均未配置，则以执行msopst命令时默认精度标准[0.01,0.05]进行比对。

否

-conf，--config_file

ST测试高级功能配置文件（msopst.ini）存储路径，可配置为绝对路径或者相对路径。

msopst.ini配置文件的详细说明请参见表2。

用户可通过修改msopst.ini配置文件，实现如下高级功能：

  - ST测试源码可编辑
  - 已编辑的ST测试源码可执行
  - 设置Host日志级别环境变量
  - 设置日志是否在控制台显示
  - 设置atc模型转换的日志级别
  - 设置atc模型转换运行环境的操作系统类型及架构
  - 设置模型精度
  - 读取算子在昇腾AI处理器上运行的性能数据

否

-err_report，--error_report

针对比对失败的用例，获取算子期望数据与实际用例执行结果不一致的数据。若未设置此参数，默认为：“false”。

  - *true：针对比对失败的用例，将算子期望数据与实际用例执行结果不一致的数据保存在{**case.name**}*_error_report.csv文件中。
  - false：不保存比对失败的数据结果。 说明：
    - *设置此参数为“true”时，获取的比对数据会根据每个case_name生成独立的csv文件，{**case.name**}**_error_report.csv文件所在目录为{output_path}**/{time_stamp}**/{op_type}*/run/out/test_data/data/st_error_reports。
    - *单个csv文件保存数据的上限为5万行，超过则依次生成新的.csv文件，文件命名如：{**case.name**}**_error_report0*.csv。

否

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
|  |  |  |
|  |  |  |

  - msopst.ini文件获取路径为：${INSTALL_DIR}/python/site-packages/bin/。
${INSTALL_DIR}请替换为CANN软件安装后文件存储路径。以root用户安装为例，则安装后文件存储路径为：/usr/local/Ascend/cann。

  - msopst.ini文件参数说明如下表所示。**表2**msopst.ini文件参数说明
参数

值

说明

only_gen_without_run

    - True
    - False（默认）

msOpST工具运行模式。

详情请参见表3。

only_run_without_gen

    - True
    - False（默认）

performance_mode

    - True
    - False

*获取算子性能模式。若设置为True，运行成功后在run/out/prof/JOBxxx*/summary目录下生成一系列性能结果文件，用户只需查看op_summary_0_1.csv即可。
该功能需要配置CANN包安装环境变量，请根据实际安装路径修改。
```
export install_path=/home/HwHiAiUser/Ascend/cann
```

ASCEND_GLOBAL_LOG_LEVEL

    - 0：DEBUG级别
    - 1：INFO级别
    - 2：WARNING级别
    - 3：ERROR级别（默认）
    - 4：NULL级别，不输出日志

设置Host日志级别环境变量。

ASCEND_SLOG_PRINT_TO_STDOUT

    - 0：屏幕不打印输出（默认）
    - 1：屏幕打印输出

日志屏幕打印控制。

atc_singleop_advance_option
--log参数取值:
    - debug：输出debug/info/warning/error/event级别的运行信息
    - info：输出info/warning/error/event级别的运行信息
    - warning：输出warning/error/event级别的运行信息
    - error：输出error/event级别的运行信息（默认）
    - null：不输出日志信息
--precision_mode参数取值:
    - force_fp16：表示算子支持fp16和fp32时，强制选择fp16（默认）
    - force_fp32：表示算子支持fp16和fp32时，强制选择fp32
    - allow_fp32_to_fp16：表示如果算子支持fp32，则保留原始精度fp32；如果不支持fp32，则选择fp16
    - must_keep_origin_dtype：表示保持原图精度
    - allow_mix_precision：表示混合精度模式

--host_env_os参数取值：

linux：表示设置操作系统类型为linux
--host_env_cpu参数取值:
    - x86_64：表示设置操作系统架构为x86_64
    - aarch64：表示设置操作系统架构为aarch64

示例：

```
atc_singleop_advance_option = "--log=info --host_env_os=linux --host_env_cpu=aarch64 --precision_mode=force_fp16"
```

设置单算子模型转换高级选项。

若模型编译环境的操作系统及其架构与模型运行环境不一致时，则需使用--host_env_os和--host_env_cpu参数设置模型运行环境的操作系统类型。如果不设置，则默认取模型编译环境的操作系统架构，即atc所在环境的操作系统架构。

HOST_ARCH

    - X86_64：X86_64架构
    - aarch64：arm64架构

示例：

```
HOST_ARCH="aarch64"
```

执行机器的架构。

一般在分设场景下配置该参数。

TOOL_CHAIN

g++ path：g++工具链路径

示例：

```
TOOL_CHAIN="/usr/bin/g++"
```

c++编译器路径，配置时以g++结尾。

一般在分设场景下配置该参数。
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
**表3**msOpST的运行模式
模式

only_gen_without_run

only_run_without_gen

运行模式

1

False

False

既生成ST测试代码，又运行ST测试代码。

2

True

True/False

只生成ST测试代码，不运行ST测试代码。

3

False

True

不生成ST测试代码，只运行ST测试代码。
|  |  |  |  |
| --- | --- | --- | --- |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |

  - **命令行执行示例：**
    - 不启用msOpST工具的高级功能，执行如下命令生成ST测试用例并执行。********
```
msopst run -i xx/Add_case_timestamp.json -soc {soc version} -out ./output
```

    - 启动msOpST工具的高级功能，仅生成ST测试用例，用户修改ST测试用例后，再执行ST测试用例。
      1. 执行命令，编辑msopst.ini文件
```
vim ${INSTALL_DIR}/python/site-packages/bin/msopst.ini
```

${INSTALL_DIR}请替换为CANN软件安装后文件存储路径。以root用户安装为例，则安装后文件存储路径为：/usr/local/Ascend/cann。

将msOpST工具的运行模式修改为模式2，按照表3修改“only_gen_without_run”和“only_run_without_gen”参数的取值。只生成ST测试代码，不运行ST测试代码。

      2. 执行如下命令生成ST测试源码。**********
```
msopst run -i xx/Add_case_timestamp.json -soc {soc version} -out ./output -conf xx/msopst.ini
```

-conf参数请修改为msopst.ini配置文件的实际路径。

ST测试用例生成后，用户可根据需要自行修改ST测试用例代码。

      3. 修改msopst.ini文件，修改运行模式为仅执行ST测试用例。
执行命令，编辑msopst.ini文件

```
vim ${INSTALL_DIR}/python/site-packages/bin/msopst.ini
```

将msOpST工具的运行模式修改为模式3，按照表3修改“only_gen_without_run”和“only_run_without_gen”参数的取值。不生成ST测试代码，只运行ST测试代码。

      4. 执行如下命令运行已修改的ST测试源码。**********
```
msopst run -i xx/Add_case_timestamp.json -soc {soc version} -out ./output -conf xx/msopst.ini
```

4. 查看执行结果。

  - 若运行模式为仅生成ST测试用例代码，不执行ST测试用例，会在-out指定的目录下生成时间戳目录，时间戳目录下将生成以算子的OpType命名的存储测试用例代码的文件夹，目录结构如下所示：****
```
 {time_stamp}
│   ├── OpType
│   │   ├── CMakeLists.txt            // 编译规则文件
│   │   ├── inc                       // 测试用例代码所用头文件
│   │   │   └── common.h
│   │   │   └── op_execute.h
│   │   │   └── op_runner.h
│   │   │   └── op_test_desc.h
│   │   │   └── op_test.h
│   │   ├── run                       // 测试用例执行相关文件存储目录
│   │   │   └── out
│   │   │       └── test_data
│   │   │          └── config
│   │   │             └── acl.json      //用于进行acl初始化，请勿修改此文件
│   │   │             └── acl_op.json   // 用于构造单算子模型文件的算子描述文件
│   │   │          └── data
│   │   │             └── expect
│   │   │             └── Test_xxx.bin
│   │   ├── src
│   │   │   └── CMakeLists.txt    // 编译规则文件
│   │   │   └── common.cpp         // 公共函数，读取二进制文件函数的实现文件 
│   │   │   └── main.cpp            // 初始化算子测试用例并执行用例
│   │   │   └── op_execute.cpp        //针对单算子调用的AscendCL接口进行了封装
│   │   │   └── op_runner.cpp         //加载单算子模型文件进行执行的接口进行了封装
│   │   │   └── op_test.cpp          //定义了算子的测试类
│   │   │   └── op_test_desc.cpp      //对算子测试用例信息的加载和读入
│   │   │   └── testcase.cpp             //测试用例的定义文件
```

  - 若运行模式为既生成ST测试代码，又运行ST测试代码，命令执行完成后，会打印测试用例执行结果，并会在-out指定的目录下生成时间戳目录，时间戳目录下将生成以算子的OpType命名的存储测试用例及测试结果的文件夹，目录结构如下所示：****
```
 {time_stamp}
│   ├── OpType
│   │   ├── build
│   │   │   └── intermediates             //编译产生中间文件
│   │   │       └── xxx
│   │   ├── CMakeLists.txt    // 编译规则文件
│   │   ├── inc
│   │   │   ├── common.h
│   │   │   ├── op_execute.h
│   │   │   ├── op_runner.h
│   │   │   ├── op_test_desc.h
│   │   │   └── op_test.h
│   │   ├── run                           // 测试用例执行相关文件存储目录
│   │   │   └── out
│   │   │       ├── fusion_result.json
│   │   │       ├── main           // 算子测试用例执行的可执行文件
│   │   │       ├── op_models         // 单算子的离线模型文件
│   │   │          ├── xx.om
│   │   │       ├── result_files
│   │   │          ├── result.txt
│   │   │          ├── Test_xxx_output_x.bin   // 运行测试用例生成的结果数据的二进制文件
│   │   │       └── test_data         //测试数据相关文件存储目录
│   │   │          ├── config
│   │   │             ├── acl_op.json    // 用于构造单算子模型文件的算子描述文件
│   │   │             ├── acl.json       //用于进行acl初始化，请勿修改此文件
│   │   │          ├── data                //构造的测试数据
│   │   │             ├──expect
│   │   │                 ├──Test_xxxx.bin      //期望的输出结果的二进制文件
│   │   │             ├──st_error_reports
│   │   │                 ├──Test_xxxx.csv       //用于保存比对结果不一致的数据
│   │   │             ├──Test_xxxx.bin      //测试数据的二进制文件
│   │   └── src
│   │       ├── CMakeLists.txt    // 编译规则文件
│   │       ├── common.cpp         // 公共函数，读取二进制文件函数的实现文件
│   │       ├── main.cpp            // 初始化算子测试用例并执行用例
│   │       ├── op_execute.cpp        //针对单算子调用的AscendCL接口进行了封装
│   │       ├── op_runner.cpp         //加载单算子模型文件进行执行的接口进行了封装
│   │       ├── op_test.cpp          //定义了算子的测试类
│   │       ├── op_test_desc.cpp      //对算子测试用例信息的加载和读入
│   │       └── testcase.cpp             //测试用例的定义文件
│   └── st_report.json        //运行报表
```

命令运行成功后会生成报表st_report.json，保存在“The st_report saved in”路径下，记录了测试的信息以及各阶段运行情况。
同时，st_report.json报表可以对比测试结果，如果用户运行出问题，也可基于报表查询运行信息，以便问题定位。**表4**st_report.json报表主要字段及含义
字段

说明

run_cmd

-

-

命令行命令。

report_list

-

-

报告列表，该列表中可包含多个测试用例的报告。

trace_detail

-

运行细节。

st_case_info

测试信息，包含如下内容。

    - expect_data_path：期望计算结果路径。
    - case_name：测试用例名称。
    - input_data_path：输入数据路径。
    - planned_output_data_paths：实际计算结果输出路径。
    - op_params：算子参数信息。

stage_result

运行各阶段结果信息，包含如下内容。

    - status：阶段运行状态，表示运行成功或者失败。
    - result：输出结果
    - stage_name：阶段名称。
    - cmd：运行命令。

case_name

-

测试名称。

status

-

测试结果状态，表示运行成功或者失败。

expect

-

期望的测试结果状态，表示期望运行成功或者失败。

summary

-

-

统计测试用例的结果状态与期望结果状态对比的结果。

test case count

-

测试用例的个数。

success count

-

测试用例的结果状态与期望结果状态一致的个数。

failed count

-

测试用例的结果状态与期望结果状态不一致的个数。
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

#### 开发环境和运行环境分设场景

1. 根据运行环境的架构在开发环境上搭建环境。

  1. [请参见环境准备](atlasopdev_16_0003.html#ZH-CN_TOPIC_0000002536800441)，根据运行环境架构安装对应的CANN开发套件包（开发环境和运行环境架构相同时，无需重复安装CANN开发套件包）。
  2. ST测试用例执行时，会使用AscendCL接口加载单算子模型文件并执行，需要在开发环境上根据运行环境的架构配置AscendCL应用编译所需其他环境变量。
    - 当开发环境和运行环境架构相同时，环境变量如下所示。**
```
export DDK_PATH=${INSTALL_DIR}
export NPU_HOST_LIB=${INSTALL_DIR}/{arch-os}/devlib
```

    - 当开发环境和运行环境架构不同时，环境变量如下所示。****
```
export DDK_PATH=${INSTALL_DIR}/{arch-os}
export NPU_HOST_LIB=${INSTALL_DIR}/{arch-os}/devlib
```


    - ${INSTALL_DIR}请替换为CANN软件安装后文件存储路径。以root用户安装为例，则安装后文件存储路径为：/usr/local/Ascend/cann。
    - *{arch-os}中**arch**表示操作系统架构（需根据运行环境的架构选择），os*表示操作系统（需根据运行环境的操作系统选择）。

2. 在开发环境启动msOpST工具的高级功能，仅生成ST测试用例。

  1. 执行命令，编辑msopst.ini文件。
```
vim ${INSTALL_DIR}/python/site-packages/bin/msopst.ini
```

${INSTALL_DIR}请替换为CANN软件安装后文件存储路径。以root用户安装为例，则安装后文件存储路径为：/usr/local/Ascend/cann。

  2. 将msOpST工具的运行模式修改为模式2，按照表3修改“only_gen_without_run”和“only_run_without_gen”参数的取值。只生成ST测试代码，不运行ST测试代码。
  3. 若开发环境和运行环境架构不同，按照表2修改“HOST_ARCH”和“TOOL_CHAIN”参数的取值。
  4. 执行如下命令生成ST测试源码。********
```
msopst run -i {*.json} -soc {soc version} -out {output path} -conf xx/msopst.ini
```

-conf参数请修改为msopst.ini配置文件的实际路径。ST测试用例生成后，用户可根据需要自行修改ST测试用例代码。

  5. *执行完成后，将在{output path}*下生成ST测试用例，并使用g++编译器生成可执行文件main。同时，屏幕打印信息中展示此次一共运行几个用例，测试用例运行的情况，并生成报表st_report.json，保存在打印信息中“The st report saved in”所示路径下，报表具体信息请参见表4。

3. [请参见环境准备](atlasopdev_16_0003.html#ZH-CN_TOPIC_0000002536800441)，在运行环境上安装CANN软件并配置所需基本环境变量。
4. 执行测试用例。

  1. 将开发环境的算子工程目录的run目录下的out文件夹拷贝至运行环境任一目录，例如上传到/home/HwHiAiUser/Ascend_project/run_add/目录下。
  2. 在运行环境中执行out文件夹下的可执行文件。进入out文件夹所在目录，执行如下命令：
```
chmod +x main
./main
```

5. 查看运行结果。

执行完成后，打印信息会显示此次用例运行的情况，如图1所示。
**图1**
运行结果

**父主题：**[基于msOpST工具进行算子ST测试](atlasopdev_10_0095.html)