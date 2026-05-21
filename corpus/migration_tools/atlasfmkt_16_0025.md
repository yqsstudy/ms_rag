---
title: "“Segmentation fault”错误"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/MigrationTool/atlasfmkt_16_0025.html"
date_collected: "2026-05-04"
category: "migration_tools"
original_path: "zh/mindstudio/830/T&ITools/MigrationTool/atlasfmkt_16_0025.html"
---

# “Segmentation fault”错误

#### 问题现象描述

运行转换后代码无报错，仅提示“Segmentation fault”信息。

#### 原因分析

**可能原因一：**

代码中引用了TensorBoard或第三方库中包含TensorBoard，以下为已知的引用TensorBoard的第三方库。

- wandb：若该库仅用来打log，可以删除该库的调用。
- transformers：该库深度绑定TensorFlow、TensorBoard。

**可能原因二：**

训练脚本中包含两个0维Tensor在不同设备上进行比较的代码，当前该比较不支持在torch_npu上运行。

#### 解决措施

**原因一解决措施：**

注释掉相关的Summary、Writer调用即可规避该错误。Summary、Writer多用于记录日志和绘图，不影响网络跑通和精度收敛。

**原因二解决措施：**

**在脚本启动命令前添加python -X faulthandler**打印线程信息，定位到具体的报错位置，进行pdb调试。来定位脚本中是否存在两个0维Tensor在不同设备上进行比较的代码，需要用户手动修改为在同一设备上进行比较，示例如下：

修改前，在CPU和NPU上进行比较：

```
1
2
3
```

```
a = torch.tensor(123)
b = torch.tensor(456).npu()
print(a == b)

```
|  |  |
| --- | --- |

修改后，添加加粗字体信息，修改为同在NPU上进行比较：

```
1
2
3
```

```
a = torch.tensor(123).npu()
b = torch.tensor(456).npu()
print(a == b)

```
|  |  |
| --- | --- |
**父主题：**[FAQ](atlasfmkt_16_0024.html)