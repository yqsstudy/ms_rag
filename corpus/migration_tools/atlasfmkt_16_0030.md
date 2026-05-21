---
title: "快速入门"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/MigrationTool/atlasfmkt_16_0030.html"
date_collected: "2026-05-04"
category: "migration_tools"
original_path: "zh/mindstudio/830/T&ITools/MigrationTool/atlasfmkt_16_0030.html"
---

# 快速入门

#### 简介

PyTorch GPU2Ascend工具可将基于GPU的训练脚本迁移为支持NPU的脚本，大幅度提高脚本迁移速度，降低开发者的工作量。本样例可以让开发者快速体验自动迁移（推荐）和PyTorch GPU2Ascend工具的迁移效率。

本样例选用ResNet50模型，数据集为ImageNet。

#### 前提条件

- [准备一台基于Atlas 训练系列产品的训练服务器，并安装对应的驱动和固件。驱动和固件的安装请参考安装NPU驱动和固件](https://www.hiascend.com/document/detail/zh/canncommercial/850/softwareinst/instg/instg_0005.html?Mode=PmIns&InstallType=local&OS=openEuler)。
- [安装开发套件包Ascend-cann-toolkit及ops算子包，具体请参考安装CANN](https://www.hiascend.com/document/detail/zh/canncommercial/850/softwareinst/instg/instg_0008.html?Mode=PmIns&InstallType=local&OS=openEuler)。
- [以安装PyTorch 2.1.0版本为例，具体操作请参考“安装PyTorch](https://www.hiascend.com/document/detail/zh/Pytorch/730/configandinstg/instg/docs/zh/installation_guide/installation_via_binary_package.md)”章节，完成PyTorch框架和torch_npu插件的安装。
- **使用PyTorch GPU2Ascend迁移前须执行如下命令安装依赖，如下命令如果使用非root用户安装，需要在安装命令后加上--user**，例如：pip3 install pandas --user。
```
pip3 install pandas         #必选，pandas版本号需大于或等于1.2.4
pip3 install libcst         #必选，语义分析库，用于解析Python文件
pip3 install prettytable    #必选，将数据可视化为图表形式
pip3 install jedi           #必选，用于跨文件解析
```

- [下载main.py](https://gitee.com/ascend/mstt/blob/master/sample/transfer_to_npu/main.py)文件，将获得ResNet50模型放到用户自定义路径下（如/home/user）。

#### 自动迁移（推荐）

修改内容少，只需在训练脚本中导入库代码，迁移后直接在昇腾NPU平台上运行。

1. [在训练脚本main.py](https://gitee.com/ascend/mstt/blob/master/sample/transfer_to_npu/main.py)文件中导入自动迁移的库代码。
********
```
from torch.utils.data import Subset
import torch_npu 
from torch_npu.contrib import transfer_to_npu   
.....
```

2. 切换目录至迁移完成后的训练脚本所在路径（以/home/user为例），执行以下命令使用虚拟数据集进行训练，迁移完成后的训练脚本可在NPU上正常运行。
开始打印迭代日志，说明训练功能迁移成功。
```
cd /home/user
python main.py -a resnet50 --gpu 1 --epochs 1 --dummy  # --gpu 1表示使用卡1，--epochs 1是指迭代次数为1
```

3. 迁移工具自动保存权重成功，说明迁移成功。

#### 使用PyTorch GPU2Ascend工具迁移

1. 进入迁移工具所在路径。
****
```
cd ${INSTALL_DIR}/cann/tools/ms_fmk_transplt/  # ${INSTALL_DIR}请替换为CANN软件安装后文件存储路径。以root用户安装为例，则安装后文件存储路径为：/usr/local/Ascend/cann。
```

2. [执行脚本迁移任务，参考表1](atlasfmkt_16_0020.html#ZH-CN_TOPIC_0000002505041560__zh-cn_topic_0000002502718150_table1581171912407)配置信息。
******
```
./pytorch_gpu2npu.sh -i /home/user -o /home/out -v 2.1.0  # /home/user为原始脚本路径， /home/out为脚本迁移结果输出路径，2.1.0为原始脚本的PyTorch框架版本
```

3. 切换目录至迁移完成后的训练脚本所在路径（以/home/user为例），执行以下命令使用虚拟数据集进行训练，迁移完成后的训练脚本可在NPU上正常运行。
开始打印迭代日志，说明训练功能迁移成功。
```
cd /home/user
python main.py -a resnet50 --gpu 1 --epochs 1 --dummy  # --gpu 1表示使用卡1，--epochs 1是指迭代次数为1
```

4. 完成脚本迁移，进入脚本迁移结果的输出路径查看结果件。

[脚本迁移过程中会启动迁移分析，默认使用torch_apis和affinity_apis的分析模式，可参见分析报告简介](atlasfmkt_16_0018.html#ZH-CN_TOPIC_0000002536921481__zh-cn_topic_0000002534398165_section63181951105910)查看对应的结果件。

5. 迁移工具自动保存权重成功，说明迁移成功。