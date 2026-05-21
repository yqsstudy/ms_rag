---
title: "GPU单卡脚本迁移为NPU多卡脚本"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/MigrationTool/atlasfmkt_16_0038.html"
date_collected: "2026-05-04"
category: "migration_tools"
original_path: "zh/mindstudio/830/T&ITools/MigrationTool/atlasfmkt_16_0038.html"
---

# GPU单卡脚本迁移为NPU多卡脚本

如果迁移时启用了“distributed”参数，想将GPU单卡脚本迁移为NPU多卡脚本，需进行如下操作获取结果文件：

将GPU单卡脚本迁移为NPU多卡脚本之后，若原模型训练命令中包含指定卡号进行单卡运行的参数（如--gpu），需要删除该参数，以确保多卡运行不失效。

1. 训练脚本语句替换。

**将执行迁移命令后生成的“run_distributed_npu.sh”文件中的please input your shell script here语句替换成模型原来的训练shell脚本。例如将“please input your shell script here*****”替换为模型训练命令“bash model_train_script.sh**--data_path data_path***”。
“run_distributed_npu.sh”文件如下所示：
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
```

```
export MASTER_ADDR=127.0.0.1 
export MASTER_PORT=29688 
export HCCL_WHITELIST_DISABLE=1    
 
NPUS=($(seq 0 7)) 
export RANK_SIZE=${#NPUS[@]} 
rank=0 
for i in ${NPUS[@]} 
do 
    export DEVICE_ID=${i} 
    export RANK_ID=${rank} 
    echo run process ${rank} 
    please input your shell script here > output_npu_${i}.log 2>&1 & 
    let rank++ 
done

```
|  |  |
| --- | --- |
**表1**run_distributed_npu.sh参数说明
参数

说明

MASTER_ADDR

指定训练服务器的IP。

MASTER_PORT

指定训练服务器的端口。

HCCL_WHITELIST_DISABLE

HCCL通信白名单校验。

NPUS

指定在特定NPU上运行。

RANK_SIZE

指定调用卡的数量。

DEVICE_ID

指定调用的device_id。

RANK_ID

指定调用卡的逻辑ID。
|  |  |
| --- | --- |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |

2. 替换后，执行“run_distributed_npu.sh”文件，会生成指定NPU的log日志。
3. 查看结果文件。

脚本迁移完成后，进入结果输出路径查看结果文件。以GPU单卡脚本迁移为NPU多卡脚本为例，结果文件包含以下内容：

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
├── xxx_msft/xxx_msft_multi              // 脚本迁移结果输出目录
│   ├── 生成脚本文件                 // 与迁移前的脚本文件目录结构一致
│   ├── msFmkTranspltlog.txt         // 脚本迁移过程日志文件,日志文件限制大小为1M,若超过限制将分多个文件进行存储,最多不会超过10个
│   ├── cuda_op_list.csv            //分析出的CUDA算子列表
│   ├── unknown_api.csv             //支持情况存疑的API列表
│   ├── unsupported_api.csv         //不支持的API列表
│   ├── change_list.csv              // 修改记录文件
│   ├── run_distributed_npu.sh       // 多卡启动shell脚本

```
|  |  |
| --- | --- |

4. 查看迁移后的py脚本，可以看到脚本中的CUDA侧API被替换成NPU侧的API。

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
28
29
30
31
32
33
34
35
36
37
```

```
def main():
    args = parser.parse_args()
 
    if args.seed is not None:
        random.seed(args.seed)
        torch.manual_seed(args.seed)
        cudnn.deterministic = True
        cudnn.benchmark = False
        warnings.warn('You have chosen to seed training. '
                      'This will turn on the CUDNN deterministic setting, '
                      'which can slow down your training considerably! '
                      'You may see unexpected behavior when restarting '
                      'from checkpoints.')
 
    if args.gpu is not None:
        warnings.warn('You have chosen a specific GPU. This will completely '
                      'disable data parallelism.')
 
    if args.dist_url == "env://" and args.world_size == -1:
        args.world_size = int(os.environ["WORLD_SIZE"])
 
    args.distributed = args.world_size > 1 or args.multiprocessing_distributed
 
    if torch_npu.npu.is_available():
        ngpus_per_node = torch_npu.npu.device_count()
    else:
        ngpus_per_node = 1
    if args.multiprocessing_distributed:
        # Since we have ngpus_per_node processes per node, the total world_size
        # needs to be adjusted accordingly
        args.world_size = ngpus_per_node * args.world_size
        # Use torch.multiprocessing.spawn to launch distributed processes: the
        # main_worker process function
        mp.spawn(main_worker, nprocs=ngpus_per_node, args=(ngpus_per_node, args))
    else:
        # Simply call main_worker function
        main_worker(args.gpu, ngpus_per_node, args)

```
|  |  |
| --- | --- |

**父主题：**[典型案例](atlasfmkt_16_0021.html)