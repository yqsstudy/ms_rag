---
title: "运行报错"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/MigrationTool/atlasfmkt_16_0029.html"
date_collected: "2026-05-04"
category: "migration_tools"
original_path: "zh/mindstudio/830/T&ITools/MigrationTool/atlasfmkt_16_0029.html"
---

# 运行报错
**表1**运行报错
报错信息

解决措施

运行报错：RuntimeError: Attempting to deserialize object on a CUDA device but torch.cuda.is_available() is False. If you are running on a CPU-only machine, please use torch.load with map_location=torch.device(‘cpu’) to map your storages to the CPU.

一般在报错代码行加入参数map_location=torch.device(‘cpu’)即可规避此问题。

运行报错：Unsupport data type: at::ScalarType::Double.

在报错代码行前添加数据类型转换语句即可规避此问题。

如报错代码行为pos = label.data.eq(1).nonzero(as_tuple =False).squeeze().npu()不支持数据类型，在代码上一行加上label = label.cpu().float().npu()进行数据类型转换。

运行报错：IndexError: invalid index of a 0-dim tensor. Use tensor.item() in Python or tensor.item<T>() in C++ to convert a 0-dim tensor to a number.

遇到类似错误直接将代码中.data[0]改成.item()。

例如将：

```
1
```

```
M = (d_loss_real + torch.abs(diff)).data[0]

```
|  |  |
| --- | --- |

改为：

```
1
```

```
M = (d_loss_real + torch.abs(diff)).item()

```
|  |  |
| --- | --- |

运行报错：Could not run ‘aten::empty_with_format’ with arguments from the ‘CPUTensorId’ backend. ‘aten::empty_with_format’ is only available for these backend "CUDA、NPU".

需要将Tensor放到NPU上，类似input = input.npu()。

运行报错：options.device().type() == DeviceType::NPU INTERNAL ASSERT FAILED xxx:

需要将Tensor放到NPU上，类似input = input.npu()。

运行报错：Attempting to deserialize object on a CUDA device but torch.cuda.is_available() is False.

此错误一般是torch.load()接口导致的，需要加关键字参数map_location，如map_location='npu’或map_location=‘cpu’。

运行报错：RuntimeError: Incoming model is an instance of torch.nn.parallel.DistributedDataParallel. Parallel wrappers should only be applied to the model(s) AFTER.

此错误是由于“torch.nn.parallel.DistributedDataParallel”接口在“apex.amp.initial”接口之前调用导致的，需要手动将“torch.nn.parallel.DistributedDataParallel”接口的调用移到“apex.amp.initial”接口调用之后即可。
**父主题：**[FAQ](atlasfmkt_16_0024.html)