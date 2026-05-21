---
title: "PyTorch GPU2Ascend工具迁移方式"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/MigrationTool/atlasfmkt_16_0020.html"
date_collected: "2026-05-04"
category: "migration_tools"
original_path: "zh/mindstudio/830/T&ITools/MigrationTool/atlasfmkt_16_0020.html"
---

# PyTorch GPU2Ascend工具迁移方式

#### 前提条件
**使用PyTorch GPU2Ascend工具执行PyTorch训练脚本迁移前须安装如下依赖。如下命令如果使用非root用户安装，需要在安装命令后加上--user****，例如：pip3 install pandas****--user**，安装命令可在任意路径下执行。
```
1
2
3
4
```

```
pip3 install pandas         #pandas版本号需大于或等于1.2.4
pip3 install libcst         #Python语法树解析器，用于解析Python文件
pip3 install prettytable    #将数据可视化为图表形式
pip3 install jedi           #可选，用于跨文件解析，建议安装

```
|  |  |
| --- | --- |

#### 使用约束

- 由于转换后的脚本与原始脚本平台不一致，迁移后的脚本在调试运行过程中可能会由于算子差异等原因而出现异常，导致进程终止，该类异常需要用户根据异常信息进一步调试解决。
- 分析迁移后可以参考原始脚本提供的训练流程进行训练。

#### 启动迁移任务

1. 进入迁移工具所在路径。
**
```
cd ${INSTALL_DIR}/cann/tools/ms_fmk_transplt/     #
${INSTALL_DIR}请替换为CANN软件安装后文件存储路径。以root用户安装为例，则安装后文件存储路径为：/usr/local/Ascend/cann。
```

2. 启动迁移任务。
参考表1配置信息，执行如下命令启动迁移任务。**********
```
./pytorch_gpu2npu.sh -i /home/username/fmktransplt -o /home/username/fmktransplt_output -v 2.1.0 [-s] [distributed -m /home/train/train.py -t model]  # /home/username/fmktransplt为原始脚本路径，/home/username/fmktransplt_output为脚本迁移结果输出路径，2.1.0为原始脚本框架版本，/home/train/train.py为训练脚本的入口文件，model为目标模型变量名
```

distributed及其参数-m、-t在语句最后指定。

参考示例：

```
#单卡
./pytorch_gpu2npu.sh -i /home/train/ -o /home/out -v 2.1.0 [-s]
#分布式
./pytorch_gpu2npu.sh -i /home/train/ -o /home/out -v 2.1.0 [-s] distributed -m /home/train/train.py [-t model]
```

“[]”表示可选参数，实际使用可不用添加。
**表1**参数说明
参数

参数说明

取值示例

-i

--input

  - 要进行迁移的原始脚本文件所在文件夹路径。
  - 必选。

/home/username/fmktransplt

-o

--output

  - 脚本迁移结果文件输出路径。
  - 不开启“distributed”即迁移至单卡脚本场景下，输出目录名为xxx_msft；开启“distributed”即迁移至多卡脚本场景下，输出目录名为xxx_msft_multi，xxx为原始脚本所在文件夹名称。
  - 必选。

/home/username/fmktransplt_output

-v

--version

  - 待迁移脚本的PyTorch版本。
  - 必选。

  - 1.11.0
  - 2.1.0
  - 2.2.0
  - 2.3.1
  - 2.4.0
  - 2.5.1
  - 2.6.0

-s

--specify-device

  - 可以通过环境变量DEVICE_ID指定device作为高级特性，但有可能导致原本脚本中分布式功能失效。
  - 可选。

-

distributed

  - **[将GPU单卡脚本迁移为NPU多卡脚本，仅支持使用torch.utils.data.DataLoader方式加载数据的场景说明](atlasfmkt_16_0023.html#ZH-CN_TOPIC_0000002504881720)**。指定此参数后，才可以指定-t/--target_model参数。
  - -m/--main：训练脚本的入口Python文件，必选。
  - -t/--target_model：待迁移脚本中的实例化模型变量名，默认为“model”，可选。
**如果变量名不为"model"时，则需要配置此参数，例如"my_model = Model()"，需要配置为-t my_model**。

-

-h

--help

打印帮助信息。

-
|  |  |  |
| --- | --- | --- |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |

3. 完成脚本迁移，进入脚本迁移结果的输出路径查看结果件。

  - [脚本迁移过程中会启动迁移分析，默认使用torch_apis和affinity_apis的分析模式，可参见分析报告简介](atlasfmkt_16_0018.html#ZH-CN_TOPIC_0000002536921481__zh-cn_topic_0000002534398165_section63181951105910)查看对应的结果件。
  - [若迁移时启用了“distributed”参数，可参见GPU单卡脚本迁移为NPU多卡脚本](atlasfmkt_16_0038.html#ZH-CN_TOPIC_0000002505041562)获取相关结果件。

4. [请参考训练配置](atlasfmkt_16_0022.html#ZH-CN_TOPIC_0000002536921483)及原始脚本提供的训练流程，在昇腾NPU平台直接运行修改后的模型脚本。
5. 成功保存权重，说明保存权重功能迁移成功。
6. 训练完成后，迁移工具自动保存权重成功，说明迁移成功。
**父主题：**[迁移训练](atlasfmkt_16_0035.html)