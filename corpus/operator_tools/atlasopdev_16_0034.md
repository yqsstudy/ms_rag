---
title: "生成单算子上板测试框架"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0034.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0034.html"
---

# 生成单算子上板测试框架

*通过指定Ascend C算子的ST测试用例定义文件（.json）和实现文件kernel_name*.cpp，自动生成调用核函数的上板测试框架，进行算子的测试验证，最终查看输出结果确认算子功能是否正确。

- 该功能仅支持Atlas 推理系列产品和Atlas 训练系列产品，不支持Atlas A2 训练系列产品/Atlas A2 推理系列产品和Atlas A3 训练系列产品。
- 所有参数不支持输入addr及tiling属性。
- 支持使用#ifndef __CCE_KT_TEST__对核函数的调用进行封装的场景。

1. 请用户完成以下输入文件的准备工作。

  - 算子ST测试用例定义文件（*.json文件）。
  - [Kernel侧算子实现文件（*.cpp文件），具体可参考《Ascend C算子开发指南](https://www.hiascend.com/document/detail/zh/canncommercial/850/opdevg/Ascendcopdevg/atlas_ascendc_map_10_0002.html)[》中的Kernel侧算子实现](https://www.hiascend.com/document/detail/zh/canncommercial/850/opdevg/Ascendcopdevg/atlas_ascendc_10_0063.html)章节。

2. [生成调用Kernel函数的测试代码，执行如下命令，具体参数介绍请参见表3](atlasopdev_16_0029.html#ZH-CN_TOPIC_0000002505040548__zh-cn_topic_0000002534506445_zh-cn_topic_0000001776778716_zh-cn_topic_0000001571310758_table20825174505717)。
**********
```
msopst ascendc_test -i xx/OpType_case.json -kernel xx/add_custom.cpp -out ./output_data
```

3. 查看执行结果。
命令执行完成后，会打印"Process finished!"提示信息，并会在-out指定的目录下生成时间戳目录，时间戳目录下将生成以算子的OpType命名的存储测试用例及测试结果的文件夹，目录结构如下所示：
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
```

```
 {time_stamp}
│   ├── OpType
│   │   ├── CMakeLists.txt     // 编译规则文件
│   │   ├── data    
│   │   │   └── xx.bin        
│   │   │   └── xx.bin
│   │   ├── data_utils.h
│   │   ├── main.cpp        // 测试框架
│   │   └── run.sh      // 调用测试框架的脚本文件
│   └── st_report.json        //运行报表

```
|  |  |
| --- | --- |

命令运行成功后，会生成报表st_report.json，记录了测试的信息以及各阶段运行情况，用户运行出问题以后，可基于报表查询运行信息，以便问题定位。同时，st_report.json报表可以对比测试结果。
st_report.json保存在如下“The st_report saved in”路径中。
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
```

```
2024-01-17 08:40:55 (3271037) - [INFO] Create 1 sub test cases for Test_AddCustom_001.
2024-01-17 08:40:55 (3271037) - [INFO] [STEP2] [data_generator.py] Generate data for testcase.
2024-01-17 08:40:55 (3271037) - [INFO] Start to generate the input data for Test_AddCustom_001_case_001_ND_float.
2024-01-17 08:40:55 (3271037) - [INFO] Generate data for testcase in $HOME/AddCustom/output/20240117084055/AddCustom/data.
2024-01-17 08:40:55 (3271037) - [INFO] [STEP3] [gen_ascendc_test.py] Generate test code of calling of kernel function for AscendC operator.
2024-01-17 08:40:55 (3271037) - [INFO] Content appended to $HOME/AddCustom/output/20240117084055/AddCustom/main.cpp successfully.
2024-01-17 08:40:55 (3271037) - [INFO] AscendC operator test code files for kernel implement have been successfully generated.
2024-01-17 08:40:55 (3271037) - [INFO] If you want to execute kernel function in Ascend aihost or cpu, please execute commands: cd $HOME/AddCustom/output/20240117084055/AddCustom && bash run.sh [KERNEL_NAME](add_custom) [SOC_VERSION](ascendxxxyy) [CORE_TYPE](AiCore/VectorCore) [RUN_MODE](cpu/npu). For example: cd $HOME/AddCustom/output/20240117084055/AddCustom && bash run.sh add_custom ascendxxxyy AiCore npu
2024-01-17 08:40:55 (3271037) - [INFO] Process finished!
2024-01-17 08:40:55 (3271037) - [INFO] The st report saved in: $HOME/AddCustom/output/20240117084055/st_report.json.

```
|  |  |
| --- | --- |
**表1**st_report.json报表主要字段及含义
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

运行各阶段结果信息，包含如下内容：

  - status：阶段运行状态，表示运行成功或者失败。
  - result：输出结果。
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

4. 修改run.sh文件中的ASCEND_HOME_DIR。
ASCEND_HOME_DIR为CANN软件包安装路径，请根据实际情况进行修改。
```
1
2
3
4
5
```

```
# 指向昇腾软件包安装地址，导出环境变量
if [ ! $ASCEND_HOME_DIR ]; then
    export ASCEND_HOME_DIR=${INSTALL_DIR}     
fi
source $ASCEND_HOME_DIR/bin/set_env.bash

```
|  |  |
| --- | --- |

5. 进入执行测试框架的脚本文件所在目录，如下命令进行测试框架代码的上板验证。
******
```
bash run.sh <kernel_name> <soc_version> <core_type> <run_mode>
```
**表2**脚本参数介绍
参数名

参数介绍

取值

<kernel_name>

Ascend C算子实现文件的文件名。

比如Add算子实现文件为add_custom.cpp，则应传入add_custom。

*<soc_version>*

算子运行的AI处理器型号。

*Atlas 训练系列产品和Atlas 推理系列产品，需按照实际使用的型号配置“ascendxxxyy*”。
说明：
  - **非Atlas A3 训练系列产品/Atlas A3 推理系列产品：在安装昇腾AI处理器的服务器执行npu-smi info****命令进行查询，获取Chip Name****信息。实际配置值为AscendChip Name，例如Chip Name***取值为xxxyy**，实际配置值为Ascendxxxyy**。当Ascendxxxyy为代码样例的路径时，需要配置为ascendxxxyy*。
  - **Atlas A3 训练系列产品/Atlas A3 推理系列产品：在安装昇腾AI处理器的服务器执行npu-smi info -t board -i***id***-c***chip_id***命令进行查询，获取Chip Name****和NPU Name****信息，实际配置值为Chip Name_NPU Name。例如Chip Name***取值为Ascendxxx***，NPU Name***取值为1234，实际配置值为Ascendxxx**_**1234。当Ascendxxx**_**1234为代码样例的路径时，需要配置为ascendxxx**_*1234。
其中：

    - **id：设备id，通过npu-smi info -l**命令查出的NPU ID即为设备id。
    - **chip_id：芯片id，通过npu-smi info -m**命令查出的Chip ID即为芯片id。

<core_type>

表明算子在AiCore上或者VectorCore上运行。

AiCore或VectorCore。

<run_mode>

表明算子以cpu模式或npu模式运行。

cpu或npu。
|  |  |  |
| --- | --- | --- |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
脚本执行完毕会出现类似如下打印，输出"succeed"字样表示完成上板验证。
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
INFO: compile op on npu succeed!
[INFO] Succeeded to exec acl api aclrtCreateContext(&context, deviceId)
[INFO] Succeeded to exec acl api aclrtCreateStream(&stream)
[INFO] Succeeded to exec acl api aclrtMallocHost((void**)(&xHost), xByteSize)
[INFO] Succeeded to exec acl api aclrtMalloc((void**)&xDevice, xByteSize, ACL_MEM_MALLOC_HUGE_FIRST)
[INFO] Succeeded to exec acl api aclrtMemcpy(xDevice, xByteSize, xHost, xByteSize, ACL_MEMCPY_HOST_TO_DEVICE)
[INFO] Succeeded to exec acl api aclrtMallocHost((void**)(&yHost), yByteSize)
[INFO] Succeeded to exec acl api aclrtMalloc((void**)&yDevice, yByteSize, ACL_MEM_MALLOC_HUGE_FIRST)
[INFO] Succeeded to exec acl api aclrtMemcpy(yDevice, yByteSize, yHost, yByteSize, ACL_MEMCPY_HOST_TO_DEVICE)
[INFO] Succeeded to exec acl api aclrtMallocHost((void**)(&zHost), zByteSize)
[INFO] Succeeded to exec acl api aclrtMalloc((void**)&zDevice, zByteSize, ACL_MEM_MALLOC_HUGE_FIRST)
[INFO] Succeeded to exec acl api aclrtSynchronizeStream(stream)
[INFO] Succeeded to exec acl api aclrtMemcpy(zHost, zByteSize, zDevice, zByteSize, ACL_MEMCPY_DEVICE_TO_HOST)
[INFO] aclrtDestroyStream successfully.
INFO: execute op on npu succeed!

```
|  |  |
| --- | --- |

**父主题：**[算子测试（msOpST）](atlasopdev_16_0028.html)