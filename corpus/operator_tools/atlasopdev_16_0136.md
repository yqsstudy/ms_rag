---
title: "检测PyTorch接口调用的算子"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0136.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0136.html"
---

# 检测PyTorch接口调用的算子

#### 前提条件

- [单击Link](https://gitee.com/ascend/samples/tree/master/operator/ascendc/0_introduction/1_add_frameworklaunch/AddCustom)获取样例工程，为进行算子检测做准备。
  - 此样例工程仅支持Python3.9，若要在其他Python版本上运行，需要修改${git_clone_path}/samples/operator/ascendc/0_introduction/1_add_frameworklaunch/PytorchInvocation目录下run_op_plugin.sh文件中的Python版本。
  - 此样例工程不支持Atlas A3 训练系列产品。
  - 下载代码样例时，需执行以下命令指定分支版本。
```
git clone https://gitee.com/ascend/samples.git -b master
```

- [已参考《Ascend Extension for PyTorch 软件安装指南](https://www.hiascend.com/document/detail/zh/Pytorch/730/configandinstg/instg/docs/zh/installation_guide/installation_description.md)》，完成PyTorch框架和torch_npu插件的安装。

#### 操作步骤

1. 执行以下命令，生成自定义算子工程，并进行Host侧和Kernel侧的算子实现。
****
```
bash install.sh -v Ascendxxxyy    # xxxyy为用户实际使用的具体芯片类型
```

2. [参考算子编译部署](atlasopdev_16_0024.html#ZH-CN_TOPIC_0000002504880720)，完成算子的编译部署。

编辑样例工程目录${git_clone_path}/samples/operator/ascendc/0_introduction/1_add_frameworklaunch/CustomOp/op_kernel下的CMakeLists.txt文件，增加编译选项-sanitizer。
****
```
add_ops_compile_options(ALL OPTIONS -sanitizer)
```

3. [进入PyTorch接入工程](https://gitee.com/ascend/samples/tree/master/operator/ascendc/0_introduction/1_add_frameworklaunch/PytorchInvocation)，使用PyTorch调用方式调用AddCustom算子工程，并按照指导完成编译。

```
1
2
3
4
```

```
PytorchInvocation
├── op_plugin_patch         
├── run_op_plugin.sh      //  5.执行样例时,需要使用
└── test_ops_custom.py    //  步骤6启动工具时,需要使用

```
|  |  |
| --- | --- |

4. 执行样例，样例执行过程中会自动生成测试数据，然后运行PyTorch样例，最后检验运行结果。

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
bash run_op_plugin.sh
-- CMAKE_CCE_COMPILER: ${INSTALL_DIR}/toolkit/tools/ccec_compiler/bin/ccec
-- CMAKE_CURRENT_LIST_DIR: ${INSTALL_DIR}/AddKernelInvocation/cmake/Modules
-- ASCEND_PRODUCT_TYPE:
  Ascendxxxyy
-- ASCEND_CORE_TYPE:
  VectorCore
-- ASCEND_INSTALL_PATH:
  /usr/local/Ascend/cann
-- The CXX compiler identification is GNU 10.3.1
-- Detecting CXX compiler ABI info
-- Detecting CXX compiler ABI info - done
-- Check for working CXX compiler: /usr/bin/c++ - skipped
-- Detecting CXX compile features
-- Detecting CXX compile features - done
-- Configuring done
-- Generating done
-- Build files have been written to: ${INSTALL_DIR}/AddKernelInvocation/build
Scanning dependencies of target add_npu
[ 33%] Building CCE object cmake/npu/CMakeFiles/add_npu.dir/__/__/add_custom.cpp.o
[ 66%] Building CCE object cmake/npu/CMakeFiles/add_npu.dir/__/__/main.cpp.o
[100%] Linking CCE executable ../../../add_npu
[100%] Built target add_npu
${INSTALL_DIR}/AddKernelInvocation
INFO: compile op on ONBOARD succeed!
INFO: execute op on ONBOARD succeed!
test pass

```
|  |  |
| --- | --- |

5. [启动msSanitizer工具拉起Python程序，进行异常检测，异常检测功能的开启原则请参见异常检测功能启用原则](atlasopdev_16_0039.html#ZH-CN_TOPIC_0000002505040558__zh-cn_topic_0000002534426413_section1051122665518)。
6. [参考内存异常报告解析](atlasopdev_16_0042.html#ZH-CN_TOPIC_0000002536920491__zh-cn_topic_0000002502746384_zh-cn_topic_0000001820455825_section164048925315)[、竞争异常报告解析](atlasopdev_16_0043.html#ZH-CN_TOPIC_0000002504880738__zh-cn_topic_0000002534426381_zh-cn_topic_0000001773496140_section1028444063620)[及未初始化异常报告解析](atlasopdev_16_0128.html#ZH-CN_TOPIC_0000002505040566__zh-cn_topic_0000002534506443_zh-cn_topic_0000001820455825_section164048925315)分析异常行为。
**父主题：**[典型案例](atlasopdev_16_0044.html)