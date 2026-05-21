---
title: "配置软链接"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_068.html"
date_collected: "2026-05-04"
category: "llm_cases"
original_path: "zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_068.html"
---

# 配置软链接

为了方便在环境中使能编译优化后的Python，可通过以下命令配置系统软链接。

```
# <default_path>为系统默认Python路径（可通过`which python`查询）
cd <default_path>

# 备份原Python二进制文件
mv python python_bak

# 创建新Python软链接
ln -s <install_path>/bin/python3 python
```

按相同方式配置pip文件。配置完成后，建议检查pip文件首行Python路径是否正确。

```
vi pip
```

完成上述操作后，即可通过Python命令调用编译优化后的Python，并通过pip命令进行包管理。
**父主题：**[Python编译优化](toolsample6_065.html)