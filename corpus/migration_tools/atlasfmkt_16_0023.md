---
title: "使用torch.utils.data.DataLoader方式加载数据的场景说明"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/MigrationTool/atlasfmkt_16_0023.html"
date_collected: "2026-05-04"
category: "migration_tools"
original_path: "zh/mindstudio/830/T&ITools/MigrationTool/atlasfmkt_16_0023.html"
---

# 使用torch.utils.data.DataLoader方式加载数据的场景说明

**torch.utils.data.DataLoader****是PyTorch中一个用于数据加载的工具类，主要用于将样本数据划分为多个小批次(batch)，以便进行训练、测试、验证等任务，查看模型脚本中的数据集加载方式是否是通过torch.utils.data.DataLoader**加载，示例代码如下：

```
import torch
from torchvision import datasets, transforms
# 定义数据转换
transform = transforms.Compose([
    transforms.ToTensor(),  # 将图像转换为张量
    transforms.Normalize((0.5,), (0.5,))  # 标准化图像
])
# 加载MNIST数据集
train_dataset = datasets.MNIST(root='./data', train=True, download=True, transform=transform)
test_dataset = datasets.MNIST(root='./data', train=False, download=True, transform=transform)
# 创建数据加载器
train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=64, shuffle=True, num_workers=4) 
test_loader = torch.utils.data.DataLoader(test_dataset, batch_size=64, shuffle=False, num_workers=4)
# 使用数据加载器迭代样本
for images, labels in train_loader:
    # 训练模型的代码
    ...
```
**父主题：**[典型案例](atlasfmkt_16_0021.html)