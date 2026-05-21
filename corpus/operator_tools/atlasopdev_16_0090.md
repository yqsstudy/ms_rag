---
title: "采集Ascend C算子的性能数据"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0090.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0090.html"
---

# 采集Ascend C算子的性能数据

展示如何使用msProf工具来上板调优一个Vector算子，该Vector算子可实现两个向量相加并输出结果的功能。

[Kernel直调](atlasopdev_16_0082.html#ZH-CN_TOPIC_0000002505040624__zh-cn_topic_0000002534506413_zh-cn_topic_0000001740005733_li12291456391)[、单算子API调用](atlasopdev_16_0082.html#ZH-CN_TOPIC_0000002505040624__zh-cn_topic_0000002534506413_zh-cn_topic_0000001740005733_li112151547153912)[和PyTorch框架](atlasopdev_16_0082.html#ZH-CN_TOPIC_0000002505040624__zh-cn_topic_0000002534506413_zh-cn_topic_0000001740005733_li146811123103813)三种算子调用场景下进行性能采集的操作步骤基本一致，本示例以Kernel直调算子调用场景为例进行介绍。

#### 前提条件

- [单击Link](https://gitee.com/ascend/samples/tree/master/operator/ascendc/0_introduction/3_add_kernellaunch/AddKernelInvocationNeo)获取样例工程，为进行算子上板和仿真调优做准备。
  - 此样例工程不支持Atlas A3 训练系列产品。
  - 下载代码样例时，需执行以下命令指定分支版本。
```
git clone https://gitee.com/ascend/samples.git -b master
```

- [参考使用前准备](atlasopdev_16_0083.html#ZH-CN_TOPIC_0000002536800585)完成相关环境变量配置。

#### 操作步骤

1. [基于样例工程的说明，并参考《Ascend C算子开发指南](https://www.hiascend.com/document/detail/zh/canncommercial/850/opdevg/Ascendcopdevg/atlas_ascendc_map_10_0002.html)[》中的基于样例工程完成Kernel直调](https://www.hiascend.com/document/detail/zh/canncommercial/850/opdevg/Ascendcopdevg/atlas_ascendc_10_0056.html)章节，完成算子编译前的准备工作。
2. 构建单算子可执行文件。

以Add算子为例，在样例工程的${git_clone_path}/samples/operator/ascendc/0_introduction/3_add_kernellaunch/AddKernelInvocationNeo目录下，执行以下命令，构建可执行文件。
************
```
bash run.sh -r npu -v <soc_version>  # 运行在昇腾设备上的算子
bash run.sh -r sim -v <soc_version>  # 运行在仿真器上的算子
```

一键式编译运行脚本完成后，在工程目录下生成NPU侧可执行文件ascendc_kernels_bbit。

  - 本示例中可执行文件的名称（ascendc_kernels_bbit）仅为示例，具体以当前工程中用户实际编译的脚本为准。
  - **在安装昇腾AI处理器的服务器上执行npu-smi info****命令进行查询，获取Chip Name****信息。实际配置值为AscendChip Name，例如Chip Name***取值为xxxyy**，实际配置值为Ascendxxxyy*。

3. 导入环境变量。

```
export LD_LIBRARY_PATH=${git_clone_path}/samples/operator/ascendc/0_introduction/3_add_kernellaunch/AddKernelInvocationNeo/out/lib/:$LD_LIBRARY_PATH
```

4. 采集算子性能数据。

[对于运行在昇腾设备上的算子，使用如下命令完成msprof op](atlasopdev_16_00851.html#ZH-CN_TOPIC_0000002536920559__zh-cn_topic_0000002534426389_section0449171943115)性能数据和精细化调优数据的采集。

```
msprof op ascendc_kernels_bbit
```

[对于运行在仿真器上的算子，使用如下命令完成msprof op simulator](atlasopdev_16_00851.html#ZH-CN_TOPIC_0000002536920559__zh-cn_topic_0000002534426389_section8684154219309)性能数据、流水图和热点图数据的采集。
****
```
msprof op simulator --soc-version=Ascendxxxyy ascendc_kernels_bbit  // xxxyy为用户实际使用的具体芯片类型
```

5. [查看算子性能数据，具体请参见工具使用](atlasopdev_16_00851.html#ZH-CN_TOPIC_0000002536920559)章节。
**父主题：**[典型案例](atlasopdev_16_0089.html)