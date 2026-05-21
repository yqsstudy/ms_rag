---
title: "自动迁移方式"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/MigrationTool/atlasfmkt_16_0019.html"
date_collected: "2026-05-04"
category: "migration_tools"
original_path: "zh/mindstudio/830/T&ITools/MigrationTool/atlasfmkt_16_0019.html"
---

# 自动迁移方式

本章节将指导用户将PyTorch训练脚本从GPU平台迁移至昇腾NPU平台。自动迁移方式支持PyTorch 1.11.0、2.1.0、2.2.0、2.3.1、2.4.0、2.5.1、2.6.0版本的训练脚本的迁移，自动迁移方式较简单，且修改内容最少，只需在训练脚本中导入库代码。

自动迁移方式的情况下，PyTorch 1.11.0版本不支持Atlas A3 训练系列产品/Atlas A3 推理系列产品。

#### 使用约束

- **由于自动迁移工具使用了Python的动态特性，但torch.jit.script****不支持Python的动态语法，因此用户原训练脚本中包含torch.jit.script****时使用自动迁移功能会产生冲突。目前自动迁移时会屏蔽torch.jit.script功能，若用户脚本中必须使用torch.jit.script**[功能，请使用PyTorch GPU2Ascend工具迁移方式](atlasfmkt_16_0020.html#ZH-CN_TOPIC_0000002505041560)进行迁移。
- [自动迁移工具与昇腾已适配的三方库可能存在功能冲突，若发生冲突，请使用PyTorch GPU2Ascend工具迁移方式](atlasfmkt_16_0020.html#ZH-CN_TOPIC_0000002505041560)进行迁移。
- **当前自动迁移暂不支持channel_last****特性，建议用户使用contiguous**进行替换。
- 若原脚本中使用的backend为nccl，在init_process_group初始化进程组后，backend已被自动迁移工具替换为hccl。如果后续代码逻辑包含backend是否为nccl的判断，例如assert backend in ['gloo', 'nccl']、if backend == 'nccl'，请手动将字符串nccl改写为hccl。
- **若用户训练脚本中包含昇腾NPU平台不支持的torch.cuda.default_generators****接口，需要手动修改为torch_npu.npu.default_generators**接口。

#### 迁移操作

1. 导入自动迁移的库代码。

**在训练入口.py**文件的首行，插入以下引用内容。例如train.py中的首行插入以下引用内容。
************
```
import torch
import torch_npu
from torch_npu.contrib import transfer_to_npu   
.....
```

2. [迁移操作完成。请参考训练配置](atlasfmkt_16_0022.html#ZH-CN_TOPIC_0000002536921483)及原始脚本提供的训练流程，在昇腾NPU平台直接运行修改后的模型脚本。
3. 训练完成后，迁移工具自动保存权重成功，说明迁移成功。若迁移失败，请参考迁移异常处理进行解决。

#### 迁移异常处理

- 如果模型包含评估、在线推理功能，也可在对应脚本中导入自动迁移库代码，并通过对比评估推理结果和日志打印情况，判断与GPU、CPU是否一致决定是否迁移成功。
- 若训练过程中提示部分CUDA接口报错，可能是部分API（算子API或框架API）不支持引起，用户可参考以下方案进行解决。
  - [使用分析迁移工具对模型脚本进行分析，获得支持情况存疑的API列表，进入昇腾开源社区](https://gitcode.com/Ascend/pytorch)提出ISSUE求助。
  - [Ascend C算子请参考基于OpPlugin算子适配开发](https://www.hiascend.com/document/detail/zh/Pytorch/600/modthirdparty/modparts/thirdpart_0012.html)[《Ascend Extension for PyTorch 套件与三方库支持清单](https://www.hiascend.com/document/detail/zh/Pytorch/730/modthirdparty/modparts/thirdpart_0003.html)》中的“套件与三方库支持清单 > 昇腾自研插件 > 基于OpPlugin算子适配开发”章节进行算子适配。
  - 将部分不支持的API移动至CPU运行，方法如下：
该方法仅适用于PyTorch 1.11.0版本。

    1. [参见“方式二：源码编译安装](https://www.hiascend.com/document/detail/zh/Pytorch/730/configandinstg/instg/docs/zh/installation_guide/compilation_installation_using_source_code.md)[”《Ascend Extension for PyTorch 软件安装指南](https://www.hiascend.com/document/detail/zh/Pytorch/730/configandinstg/instg/docs/zh/installation_guide/installation_description.md)》中的“安装PyTorch > 方式二：源码编译安装”章节，获取Ascend PyTorch源码包。
    2. 进入获取后的源码包目录，修改“npu_native_functions.yaml”。
```
cd pytorch/torch_npu/csrc/aten
vi npu_native_functions.yaml
```

在“tocpu”配置下添加算子API名称。

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
tocpu:
  - angle
  - mode
  - nanmedian.dim_values
  - nansum
  - native_dropout
  - native_dropout_backward
  - poisson
  - vdot
  - view_as_complex
  - view_as_real

```
|  |  |
| --- | --- |

    3. [参见“方式二：源码编译安装](https://www.hiascend.com/document/detail/zh/Pytorch/730/configandinstg/instg/docs/zh/installation_guide/compilation_installation_using_source_code.md)[”《Ascend Extension for PyTorch 软件安装指南](https://www.hiascend.com/document/detail/zh/Pytorch/730/configandinstg/instg/docs/zh/installation_guide/installation_description.md)》中的“安装PyTorch > 方式二：源码编译安装”章节重新编译框架插件包并安装。
    4. 重新执行迁移后的训练脚本，确认模型是否能正常训练。

**父主题：**[迁移训练](atlasfmkt_16_0035.html)