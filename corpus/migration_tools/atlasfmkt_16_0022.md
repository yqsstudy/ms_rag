---
title: "训练配置"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/MigrationTool/atlasfmkt_16_0022.html"
date_collected: "2026-05-04"
category: "migration_tools"
original_path: "zh/mindstudio/830/T&ITools/MigrationTool/atlasfmkt_16_0022.html"
---

# 训练配置

本章节主要介绍在特殊场景中进行模型迁移训练时需要注意的配置事项。

- [为了提升模型运行速度，建议开启使用二进制算子，请参考安装CANN](https://www.hiascend.com/document/detail/zh/canncommercial/850/softwareinst/instg/instg_0008.html?Mode=PmIns&InstallType=local&OS=openEuler)章节安装二进制kernels算子包后，参考如下方式开启：
  - 单卡场景下，修改训练入口文件例如main.py文件，在import torch_npu下方添加如下加粗字体代码。****
```
import torch
import torch_npu
torch_npu.npu.set_compile_mode(jit_compile=False)
......
```

  - 多卡场景下，如果拉起多卡训练的方式为mp.spawn，则torch_npu.npu.set_compile_mode(jit_compile=False)必须加在进程拉起的主函数中才能使能二进制，否则使能方式与单卡场景相同。
```
1
2
3
4
5
6
7
8
```

```
if is_distributed:
    mp.spawn(main_worker, nprocs=ngpus_per_node, args=(ngpus_per_node, args))
else:
    main_worker(args.gpu, ngpus_per_node, args)
def main_worker(gpu, ngpus_per_node, args):
    # 加在进程拉起的主函数中
   torch_npu.npu.set_compile_mode(jit_compile=False)
    ......

```
|  |  |
| --- | --- |

- **用户训练脚本中包含昇腾NPU平台不支持的torch.nn.DataParallel****接口，需要手动修改为torch.nn.parallel.DistributedDataParallel**[接口执行多卡训练，参考GPU单卡脚本迁移为NPU多卡脚本](atlasfmkt_16_0038.html#ZH-CN_TOPIC_0000002505041562)进行修改。
- **若用户训练脚本中包含昇腾NPU平台不支持的amp_C****模块，需要用户手动删除import****amp_C**相关代码内容后，再进行训练。
- **若用户训练脚本中包含torch.cuda.get_device_capability**接口，迁移后在昇腾NPU平台上运行时，会返回“None”值。
**GPU平台调用torch.cuda.get_device_capability****接口时，会返回数据类型为Tuple[int, int]的GPU算力值。而NPU平台的torch.npu.get_device_capability**接口没有相应概念，会返回“None”。若遇报错，需要用户将“None”值手动修改为Tuple[int, int]类型的固定值。

- **torch.cuda.get_device_properties**接口迁移后在昇腾NPU平台上运行时，返回值不包含minor和major属性，建议用户注释掉调用minor和major属性的代码。
**父主题：**[迁移训练](atlasfmkt_16_0035.html)