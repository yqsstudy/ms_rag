---
title: "使用前准备"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0083.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0083.html"
---

# 使用前准备

#### 环境准备

- [请参考环境准备](atlasopdev_16_0003.html#ZH-CN_TOPIC_0000002536800441)，完成相关环境变量的配置。
- [若要使用MindStudio Insight进行查看时，需要单独安装MindStudio Insight软件包，具体下载链接请参见“安装与卸载](https://www.hiascend.com/document/detail/zh/mindstudio/830/GUI_baseddevelopmenttool/msascendinsightug/Insight_userguide_0005.html)”。
- [若要使用模板库](https://gitcode.com/cann/catlass/blob/master/scripts/build.sh)[进行仿真，编译脚本需增加选项--simulator， 以simulator模式编译算子。具体操作请参见Link](https://gitcode.com/cann/catlass/blob/master/docs/tools/performance_tools.md)。
```
bash scripts/build.sh --simulator 00_basic_matmul
```

模板库场景仅适用于Atlas A2 训练系列产品/Atlas A2 推理系列产品。

#### 使用约束

- *性能数据采集时间建议在5min以内，同时推荐用户设置的内存大小在20G以上（例如容器配置：docker run --memory=20g 容器名*）。
- 请确保性能数据保存在不含软链接的当前用户目录下，否则可能引起安全问题。

#### msprof op配置

[若要实现Cache热力图跳转](atlasopdev_16_0158.html#ZH-CN_TOPIC_0000002536800589__zh-cn_topic_0000002502746412_li14516202184314)功能，需要执行以下操作：

1. 在编译算子时添加-g编译选项，具体操作请参见编译选项需添加-g。
2. [表2](atlasopdev_16_0082.html#ZH-CN_TOPIC_0000002505040624__zh-cn_topic_0000002534506413_table17624248171315)中的--aic-metrics参数使能Source选项。

#### msprof op simulator配置

msProf工具的仿真功能仅支持单卡场景，无法仿真多卡场景，代码中也只能设置0卡。若修改可见卡号，则会导致仿真失败。

- msProf工具使用--config模式进行算子仿真调优之前，需执行如下命令配置环境变量。**
```
export LD_LIBRARY_PATH=${INSTALL_DIR}/tools/simulator/Ascendxxxyy/lib:$LD_LIBRARY_PATH 
```

请根据CANN软件包实际安装路径和昇腾AI处理器的型号对以上环境变量进行修改。

- 编译选项需添加-g，使能算子代码热点图和代码调用栈功能。
  - 添加-g编译选项会在生成的二进制文件中附带调试信息，建议限制带有调试信息的用户程序的访问权限，确保只有授权人员可以访问该二进制文件。
  - 若不使用llvm-symbolizer组件提供的相关功能，输入msProf的程序编译时不包含-g即可，msProf工具则不会调用llvm-symbolizer组件的相关功能。

  - [若参考msOpGen工具创建的算子工程，需编辑算子工程op_kernel目录下的CMakeLists.txt文件，可参考创建算子工程](atlasopdev_16_0021.html#ZH-CN_TOPIC_0000002505040538)。
```
1
```

```
add_ops_compile_options(ALL OPTIONS -g)

```
|  |  |
| --- | --- |

  - [若参考完整样例，以Link](https://gitee.com/ascend/samples/tree/master/operator/ascendc/0_introduction/3_add_kernellaunch/AddKernelInvocationNeo)为例，需在样例工程目录下的“cmake/npu_lib.cmake”文件中新增以下代码。
    - 此样例工程不支持Atlas A3 训练系列产品。
    - 下载代码样例时，需执行以下命令指定分支版本。
```
git clone https://gitee.com/ascend/samples.git -b master
```

****************
```
ascendc_compile_options(ascendc_kernels_${RUN_MODE} PRIVATE
-g
-O2
)
```

  - 若是Triton算子，需通过配置以下环境变量添加-g。
```
1
```

```
export TRITON_DISABLE_LINE_INFO=0

```
|  |  |
| --- | --- |

- 使用msProf工具对PyTorch脚本的算子进行仿真调优时，不支持Python内置的print函数打印Device侧上的变量和值。
- Atlas A3 训练系列产品/Atlas A3 推理系列产品和Atlas A2 训练系列产品/Atlas A2 推理系列产品的仿真器在运行过程中，当仿真blockdim大于物理核数时，仿真器可能会出现以下报错，可以通过配置pem_config_cloud.toml文件中的core_ostd_num参数解决该问题。pem_config_cloud.toml文件的路径为${INSTALL_DIR}/tools/simulator/Ascendxxxyy/lib/pem_config_cloud.toml。****
```
[ARCH]
    cube_core_num           = 1
    vec_core_num            = 2
    core_ostd_num        = 2             # 2 early end  1 normal mode
```

#### 启动工具

- [请参见msprof op](atlasopdev_16_00851.html#ZH-CN_TOPIC_0000002536920559__zh-cn_topic_0000002534426389_section0449171943115)的操作步骤使能msProf工具的上板调优功能。
- 请先参见msprof op simulator配置[去配置部分仿真调优的功能，然后根据msprof op simulator](atlasopdev_16_00851.html#ZH-CN_TOPIC_0000002536920559__zh-cn_topic_0000002534426389_section8684154219309)的操作步骤使能msProf工具的仿真调优功能。

当前msProf不支持-O0编译选项。
**父主题：**[算子调优（msProf）](atlasopdev_16_0081.html)