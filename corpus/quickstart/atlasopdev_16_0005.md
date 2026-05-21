---
title: "算子功能测试（msOpST）"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/msquickstart/atlasopdev_16_0005.html"
date_collected: "2026-05-04"
category: "quickstart"
original_path: "zh/mindstudio/830/msquickstart/atlasopdev_16_0005.html"
---

# 算子功能测试（msOpST）

msOpST工具用于算子开发完成后，对算子功能进行初步测试，该工具可以更加高效地进行算子性能的分析和优化，提高算子的执行效率，降低开发成本。

本样例基于AscendCL接口的流程，生成单算子的OM文件，并执行该文件以验证算子执行结果的正确性。

1. 生成ST测试用例。

  1. [在创建算子工程中的步骤2](atlasopdev_16_0009.html#ZH-CN_TOPIC_0000002502590824__li9375102315016)[执行完成后，再执行以下命令，并根据msOpGen算子工程目录](atlasopdev_16_0009.html#ZH-CN_TOPIC_0000002502590824__li20608132944115)替换命令路径。
```
msopst create -i "$HOME/AddCustom/op_host/add_custom.cpp" -out ./st
```

  2. 生成ST测试用例。
```
1
2
3
4
5
```

```
2024-09-10 19:47:15 (3995495) - [INFO] Start to parse AscendC operator prototype definition in $HOME/AddCustom/op_host/add_custom.cpp.
2024-09-10 19:47:15 (3995495) - [INFO] Start to check valid for op info.
2024-09-10 19:47:15 (3995495) - [INFO] Finish to check valid for op info.
2024-09-10 19:47:15 (3995495) - [INFO] Generate test case file $HOME/AddCustom/st/AddCustom_case_20240910194715.json successfully.
2024-09-10 19:47:15 (3995495) - [INFO] Process finished!

```
|  |  |
| --- | --- |

  3. 在./st目录下生成ST测试用例。

2. 执行ST测试。

  1. 根据CANN包路径设置环境变量。********
```
export DDK_PATH=${INSTALL_DIR}
export NPU_HOST_LIB=${INSTALL_DIR}/{arch-os}/devlib  // {arch-os}中arch表示操作系统架构（需根据运行环境的架构选择），os表示操作系统（需根据运行环境的操作系统选择）
```

  2. 执行ST测试，并将输出结果到指定路径。******
```
msopst run -i ./st/AddCustom_case_{TIMESTAMP}.json -soc Ascendxxxyy -out ./st/out   // xxxyy为用户实际使用的具体芯片类型
```

    - ${INSTALL_DIR}请替换为CANN软件安装后文件存储路径。以root用户安装为例，则安装后文件存储路径为：/usr/local/Ascend/cann。

3. *测试成功后，将测试结果输出在./st/out/{TIMESTAMP}*[/路径下的st.report.json文件，具体请参见《算子开发工具用户指南](https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0002.html)[》的“算子测试（msOpST）> 生成/执行测试用例](https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0033.html)”章节。
**父主题：**[算子开发工具快速入门](tools_qucikstart_0006.html)