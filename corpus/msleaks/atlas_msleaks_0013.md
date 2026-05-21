---
title: "内存块监测"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/msleaks/atlas_msleaks_0013.html"
date_collected: "2026-05-04"
category: "msleaks"
original_path: "zh/mindstudio/830/T&ITools/msleaks/atlas_msleaks_0013.html"
---

# 内存块监测

大模型场景下，单卡的计算任务十分复杂，如果内存踩踏发生，定位非常困难。msLeaks工具支持通过Python接口在算子执行前后监测指定内存块，根据内存块数据的变化，定位算子间内存踩踏的范围或具体位置。

#### 使用方法

1. 执行以下命令，关闭多任务下发。

```
export ASCEND_LAUNCH_BLOCKING=1
```

2. 执行以下命令，开启内存块监测。
**
```
msleaks ${Application} --watch=start:outid,end,full-content
```

  - **内存块监测功能仅支持Aten单算子和ATB算子，且可以通过--level**指定op维度和kernel维度的内存块监测。
  - Ascend Extension for PyTorch场景下，kernel算子的监测仅支持调用Python接口的方式，暂不支持watch命令行方式。调用Python接口的监测方式请参见3。
  - 需控制内存监测算子的范围和内存块大小，避免由于设置过大，导致的dump数据耗时增加，以及磁盘空间占用过多的问题。
**表1**参数说明
参数

说明

Application

用户的可执行脚本。

如果需要使用Python接口指定被监测的Tensor，具体设置请参见3。

--watch

开启内存块监测功能。

  - start：可选，字符串形式，表示开始监测算子。
  - outid：可选，表示算子的output编号。当Tensor为一个列表时，可以指定需要落盘的Tensor，取值为Tensor在列表中的下标编号。
  - end：必选，字符串形式，表示结束监测算子。
  - full-content：可选，表示全量落盘内存数据，会将每个Tensor对应的二进制文件进行落盘。如果不选择该值，表示轻量化落盘，仅落盘Tensor对应的哈希值。

示例：

--watch=token0/layer0/module0/op0,token0/layer0/module0/op1,full-content
|  |  |
| --- | --- |
|  |  |
|  |  |

3. 在用户的可执行脚本中，调用Python接口指定被监测的Tensor。

增加Python的watcher模块的接口，其中watch接口表示开始监测该内存块，remove接口表示取消监测该内存块。内存块监测有两种开启方式，示例代码中的参数说明可参见表2所示。

  - 方式一：直接输入Tensor
示例脚本如下：

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
```

```
import torch
import torch_npu
import msleaks

torch.npu.synchronize()
test_tensor = torch.randn(2,3).to('npu:0')        # 请根据实际情况自行创建或选择需要监测的Tensor
msleaks.watcher.watch(test_tensor, name="test", dump_nums=2)
...
torch.npu.synchronize()
msleaks.watcher.remove(test_tensor)

```
|  |  |
| --- | --- |

  - 方式二：输入内存块的地址和长度示例脚本如下：
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
```

```
import torch
import torch_npu
import msleaks

torch.npu.synchronize()
test_tensor = torch.randn(2,3).to('npu:0')       
msleaks.watcher.watch(test_tensor.data_ptr(), length=1000, name="test", dump_nums=2)
...
torch.npu.synchronize()
msleaks.watcher.remove(test_tensor.data_ptr(), length=1000)

```
|  |  |
| --- | --- |

建议使用方式一指定被监测的Tensor。如果需要使用方式二，需自行确认内存块地址和长度的有效性。

**表2**开启内存块监测的参数说明
参数

说明

name

必选，用来最后dump的时候标识监测的Tensor。

dump_nums

可选，表示指定dump的次数，不输入取值表示无限制。

test_tensor.data_ptr()

必选，表示被监测Tensor的地址。

仅当使用方式二开启内存块监测时需输入该参数。

length

必选，表示输入监测内存块的长度，当输入length时，无关键字的参数只能为地址整型变量。length的大小建议小于等于已知被监测Tensor的内存块的大小。

仅当使用方式二开启内存块监测时需输入该参数。
|  |  |
| --- | --- |
|  |  |
|  |  |
|  |  |
|  |  |

4. 命令执行完成后，内存块监测生成的结果目录如下。
****************
```
├── leaksDumpResults             
│    └── watch_dump
      │    ├── {deviceid}_{tid}_{opName}_{调用次数}-{watchedOpName}_{outid}_{before/after}.bin        # 当输入full-content参数时，落盘bin文件
      │    ├── watch_dump_data_check_sum_{deviceid}_{timestamp}.csv         # 当未输入full-content参数时，落盘csv文件
```

#### 结果说明

内存块监测功能输出的文件为bin文件或csv文件。

- bin文件记录的是Tensor的详细落盘结果。
- csv文件仅记录了Tensor对应的哈希值。
**父主题：**[内存分析](atlas_msleaks_0004.html)