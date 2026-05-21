---
title: "环境准备"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/MigrationTool/atlasfmkt_16_0017.html"
date_collected: "2026-05-04"
category: "migration_tools"
original_path: "zh/mindstudio/830/T&ITools/MigrationTool/atlasfmkt_16_0017.html"
---

# 环境准备

#### 环境准备

- [安装开发套件包，请参见《CANN 软件安装指南](https://www.hiascend.com/document/detail/zh/canncommercial/850/softwareinst/instg/instg_0000.html?Mode=PmIns&InstallType=local&OS=openEuler)》。
- 配置环境变量。***安装CANN软件后，使用CANN运行用户进行编译、运行时，需要以CANN运行用户登录环境，执行source ${install_path}*/set_env.sh**命令设置环境变量。其中${install_path}为CANN软件的安装目录，例如：/usr/local/Ascend/cann。
上述环境变量只在当前窗口生效，用户可以将上述命令写入~/.bashrc文件，使其永久生效，操作如下：

  1. **以安装用户在任意目录下执行vi ~/.bashrc****，打开.bashrc**文件，并在该文件最后添加上述环境变量。
  2. **执行:wq!**命令，保存文件并退出。
  3. **执行source ~/.bashrc**命令，使环境变量生效。

#### 使用约束

- 分析和迁移工具当前支持PyTorch1.11.0、2.1.0、2.2.0、2.3.1、2.4.0、2.5.1、2.6.0版本训练脚本的分析和迁移。
自动迁移方式的情况下，PyTorch 1.11.0版本不支持Atlas A3 训练系列产品/Atlas A3 推理系列产品。

- 原脚本需要在GPU环境下且基于Python3.7及以上能够运行成功。
- 分析迁移后的执行逻辑与迁移前需保持一致。
- [若原始代码中调用了三方库，迁移过程可能会存在适配问题。在迁移原始代码前，用户需要根据已调用的三方库，自行安装昇腾已适配的三方库版本，已适配的三方库信息和使用指南请参考《Ascend Extension for PyTorch 套件与三方库支持清单](https://www.hiascend.com/document/detail/zh/Pytorch/730/modthirdparty/modparts/thirdpart_0003.html)》。
- APEX中使用的FusedAdam优化器不支持使用自动迁移和PyTorch GPU2Ascend工具进行迁移，若原始代码中包含该优化器，用户需自行修改。
- [当前分析工具不支持对原生函数self.dropout()、nn.functional.softmax()、torch.add、bboexs_diou()、bboexs_giou()、LabelSmoothingCrossEntropy()或ColorJitter进行亲和API分析，若原训练脚本涉及以上原生函数，请参考《Ascend Extension for PyTorch 自定义API参考](https://www.hiascend.com/document/detail/zh/Pytorch/730/apiref/torchnpuCustomsapi/docs/context/overview.md)*》中“PyTorchx.x.x*> Ascend Extension for PyTorch自定义API > torch_npu.contrib”节点进行分析和替换。
- **若用户训练脚本中包含昇腾NPU平台不支持的amp_C**模块，需要用户手动删除import amp_C相关代码内容后，再进行训练。
- 由于转换后的脚本与原始脚本平台不一致，迁移后的脚本在调试运行过程中可能会由于算子差异等原因而抛出异常，导致进程终止，该类异常需要用户根据异常信息进一步调试解决。

#### 安全注意事项

- 在linux环境使用工具时，出于安全性及权限最小化角度考虑，本工具不应使用root等高权限账户进行操作，建议使用普通用户权限安装执行。
- 在linux环境使用工具时，请确保使用前执行用户的umask值大于等于0027，否则可能会造成工具生成的数据文件和目录权限过大。
- 在linux环境使用工具时，用户须自行保证使用最小权限原则，如给工具输入的文件要求other用户不可写，在一些对安全要求更严格的功能场景下还需确保输入的文件group用户不可写。
- 由于本工具依赖CANN，为保证安全，应使用同一低权限用户默认安装的CANN包，source命令执行后请不要随意修改set_env.sh中涉及的环境变量。
- 本工具为开发调测工具，不建议在生产环境使用。