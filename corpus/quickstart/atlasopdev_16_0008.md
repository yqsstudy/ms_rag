---
title: "算子调优（msProf）"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/msquickstart/atlasopdev_16_0008.html"
date_collected: "2026-05-04"
category: "quickstart"
original_path: "zh/mindstudio/830/msquickstart/atlasopdev_16_0008.html"
---

# 算子调优（msProf）

msProf工具主要作用于算子开发的性能优化阶段，通过使用msProf工具，开发者可以确保算子在不同硬件平台上都能高效运行，从而提高软件的整体性能和用户体验。

1. 在${git_clone_path}/samples/operator/ascendc/0_introduction/1_add_frameworklaunch目录下执行以下命令，生成自定义算子工程，进行host侧和kernel侧的算子实现。
****
```
bash install.sh -v Ascendxxxyy    # xxxyy为用户实际使用的具体芯片类型
```

2. 在${git_clone_path}/samples/operator/ascendc/0_introduction/1_add_frameworklaunch/CustomOp目录下执行以下命令行，重新编译部署算子。
********
```
bash build.sh
./build_out/custom_opp_<target_os>_<target_architecture>.run   // 当前目录下run包的名称
```

3. 切换到${git_clone_path}/samples/operator/ascendc/0_introduction/1_add_frameworklaunch/AclNNInvocation目录，执行以下命令生成可执行文件。

```
./run.sh
```

4. 指定算子依赖的动态库路径，将动态库so文件加载进来。

```
export LD_LIBRARY_PATH=${INSTALL_DIR}/opp/vendors/customize/op_api/lib:$LD_LIBRARY_PATH
```

5. 使用msProf工具进行调优。

  - 使用msprof op进行上板调优。
    1. 切换到${git_clone_path}/samples/operator/ascendc/0_introduction/1_add_frameworklaunch/AclNNInvocation/output目录，执行以下命令，开启上板调优。
```
msprof op --output=./output_data ./execute_add_op
```

    2. 生成以下结果目录。
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
OPPROF_{timestamp}_XXX/
├── ArithmeticUtilization.csv
├── dump
├── L2Cache.csv
├── Memory.csv
├── MemoryL0.csv
├── MemoryUB.csv
├── OpBasicInfo.csv
├── PipeUtilization.csv
├── ResourceConflictRatio.csv
└── visualize_data.bin

```
|  |  |
| --- | --- |

    3. [将visualize_data.bin文件导入MindStudio Insight工具，将上板结果可视化，具体请参见《算子开发工具用户指南](https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0002.html)[》的“算子调优（msProf）> 工具使用](https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_00851.html)”章节的msprof op。

  - 使用msprof op simulator进行仿真调优。
    1. [请参考《算子开发工具用户指南](https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0002.html)[》的“算子调优（msProf）> 使用前准备](https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0083.html)”章节，完成msprof op simulator配置。
    2. 进入${git_clone_path}/samples/operator/ascendc/0_introduction/1_add_frameworklaunch/AclNNInvocation/output目录，执行以下命令，开启仿真调优。**
```
msprof op simulator --soc-version=Ascendxxxyy --output=./output_data ./execute_add_op
```

    3. 生成以下结果目录。
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
```

```
OPPROF_{timestamp}_XXX/
├── dump
└── simulator
    ├── core0.veccore0
    ├── core0.veccore1
    ├── core1.veccore0
    ├── core1.veccore1
    ├── core2.veccore0
    ├── core2.veccore1
    ├── core3.veccore0
    ├── core3.veccore1
    ├── trace.json
    └── visualize_data.bin

```
|  |  |
| --- | --- |

    4. [将trace.json和visualize_data.bin文件导入MindStudio Insight工具，将仿真结果可视化，具体请参见《算子开发工具用户指南](https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0002.html)[》的“算子调优（msProf）> 工具使用](https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_00851.html)”章节的msprof op simulator。

**父主题：**[算子开发工具快速入门](tools_qucikstart_0006.html)