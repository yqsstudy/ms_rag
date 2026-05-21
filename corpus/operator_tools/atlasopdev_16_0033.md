---
title: "生成/执行测试用例"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0033.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0033.html"
---

# 生成/执行测试用例

指导用户根据算子测试用例定义文件生成ST测试数据及测试用例执行代码，在硬件环境上执行算子测试用例。

#### 开发环境与运行环境合设场景

1. ST测试用例执行时，会使用AscendCL接口加载单算子模型文件并执行，所以需要配置AscendCL应用编译所需其他环境变量，如下所示。

**
```
export DDK_PATH=${INSTALL_DIR}
export NPU_HOST_LIB=${INSTALL_DIR}/{arch-os}/devlib
```

  - ${INSTALL_DIR}请替换为CANN软件安装后文件存储路径。以root用户安装为例，则安装后文件存储路径为：/usr/local/Ascend/cann。
  - *{arch-os}中**arch**表示操作系统架构，os*表示操作系统。

2. [执行如下命令生成/执行测试用例，具体参数介绍请参见表2](atlasopdev_16_0029.html#ZH-CN_TOPIC_0000002505040548__zh-cn_topic_0000002534506445_zh-cn_topic_0000001821790281_table1735410430919)。

************
```
msopst run -i {*.json}  -soc {soc version}  -out {output path} -c {case name} -d {device id} -conf {msopst.ini path} -err_thr "[threshold1,threshold2]"
```

  - msopst.ini文件的路径为：${INSTALL_DIR}/python/site-packages/bin/。
  - msopst.ini文件参数说明如下表所示。
msopst.ini文件默认使用FP16精度模式，如需使用其他精度模式需手动修改表1中atc_singleop_advance_option的--precision_mode参数。
**表1**msopst.ini文件参数说明
参数

值

说明

only_gen_without_run

    - True
    - False（默认）

msOpST工具运行模式。

详情请参见表2。

only_run_without_gen

    - True
    - False（默认）

performance_mode

    - True
    - False

*获取算子性能模式。若设置为True，运行成功后在run/out/prof/JOBxxx*/summary目录下生成一系列性能结果文件，用户只需查看op_summary_0_1.csv即可。
该功能需要配置CANN包安装环境变量，请根据实际安装路径修改。
```
export install_path=${INSTALL_DIR}
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
--host_env_cpu参数取值：x86_64，表示设置操作系统架构为x86_64
    - aarch64：表示设置操作系统架构为aarch64

示例：

```
atc_singleop_advance_option="--log=info --host_env_os=linux --host_env_cpu=aarch64 --precision_mode=force_fp16"
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
**表2**msOpST的运行模式
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
msopst run -i xx/AddCustom_case_timestamp.json -soc {soc version} -out ./output
```

    - 启动msOpST工具的高级功能，仅生成ST测试用例，用户修改ST测试用例后，再执行ST测试用例。
      1. 执行命令，编辑msopst.ini文件
```
vim ${INSTALL_DIR}/python/site-packages/bin/msopst.ini
```

将msOpST工具的运行模式修改为模式2，按照表2修改“only_gen_without_run”和“only_run_without_gen”参数的取值。只生成ST测试代码，不运行ST测试代码。

      2. 执行如下命令生成ST测试源码。**********
```
msopst run -i xx/AddCustom_case_timestamp.json -soc {soc version} -out ./output -conf xx/msopst.ini
```

-conf参数请修改为msopst.ini配置文件的实际路径。

ST测试用例生成后，用户可根据需要自行修改ST测试用例代码。

      3. 修改msopst.ini文件，修改运行模式为仅执行ST测试用例。
执行命令，编辑msopst.ini文件

```
vim ${INSTALL_DIR}/python/site-packages/bin/msopst.ini
```

将msOpST工具的运行模式修改为模式3，按照表2修改“only_gen_without_run”和“only_run_without_gen”参数的取值。不生成ST测试代码，只运行ST测试代码。

      4. 执行如下命令运行已修改的ST测试源码。**********
```
msopst run -i xx/AddCustom_case_timestamp.json -soc {soc version} -out ./output -conf xx/msopst.ini
```


若执行失败。

      - [请参见“aclError](https://www.hiascend.com/document/detail/zh/canncommercial/850/API/appdevgapi/aclcppdevg_03_1345.html)”查看aclError的含义。
      - [请参见“错误码参考](https://www.hiascend.com/document/detail/zh/canncommercial/850/maintenref/troubleshooting/troubleshooting_0225.html)”。
      - [请参见《日志参考](https://www.hiascend.com/document/detail/zh/canncommercial/850/maintenref/logreference/logreference_0001.html)》查看日志进行分析。

3. 查看执行结果。

  - 若运行模式为仅生成ST测试用例代码，不执行ST测试用例，会在-out指定的目录下生成时间戳目录，时间戳目录下将生成以算子的OpType命名的存储测试用例代码的文件夹，目录结构如下所示：
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
```

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
|  |  |
| --- | --- |

  - 若运行模式为既生成ST测试代码，又运行ST测试代码，命令执行完成后，会打印测试用例执行结果，并会在-out指定的目录下生成时间戳目录，时间戳目录下将生成以算子的OpType命名的存储测试用例及测试结果的文件夹，目录结构如下所示：
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
```

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
|  |  |
| --- | --- |
命令运行成功后，会生成报表st_report.json，记录了测试的信息以及各阶段运行情况，用户运行出问题以后，可基于报表查询运行信息，以便问题定位。同时，st_report.json报表可以对比测试结果。st_report.json保存在图1中“The st_report saved in”路径下。**图1**
![](figure/zh-cn_image_0000002534506583.png "点击放大")运行结果示例**表3**st_report.json报表主要字段及含义
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

#### 开发环境与运行环境分设场景

1. 根据运行环境的架构在开发环境上搭建环境。

  1. ST测试用例执行时，会使用AscendCL接口加载单算子模型文件并执行，需要在开发环境上根据运行环境的架构配置AscendCL应用编译所需其他环境变量。
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

  2. 将msOpST工具的运行模式修改为模式2，按照表2修改“only_gen_without_run”和“only_run_without_gen”参数的取值。只生成ST测试代码，不运行ST测试代码。
  3. 若开发环境和运行环境架构不同，按照表1修改“HOST_ARCH”和“TOOL_CHAIN”参数的取值。
  4. 执行如下命令生成ST测试源码。********
```
msopst run -i xx/AddCustom_case_timestamp.json -soc {soc version} -out {output path} -conf xx/msopst.ini
```

-conf参数请修改为msopst.ini配置文件的实际路径。

ST测试用例生成后，用户可根据需要自行修改ST测试用例代码。

  5. *执行完成后，将在{output path}*下生成ST测试用例，并使用g++编译器生成可执行文件main。同时，屏幕打印信息中展示此次一共运行几个用例，测试用例运行的情况，并生成报表st_report.json，保存在打印信息中“The st report saved in”所示路径下，报表具体信息请参见表3。

3. 执行测试用例。

  1. 将开发环境的算子工程目录的run目录下的out文件夹拷贝至运行环境任一目录，例如上传到${INSTALL_DIR}/Ascend_project/run_add/目录下。
  2. 在运行环境中执行out文件夹下的可执行文件。进入out文件夹所在目录，执行如下命令：
```
chmod +x main
./main
```

4. 查看运行结果。

执行完成后，打印信息提示此次用例运行的情况，如图2所示。
**图2**
运行结果

**父主题：**[算子测试（msOpST）](atlasopdev_16_0028.html)