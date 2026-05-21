---
title: "引用库找不到的问题"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/MigrationTool/atlasfmkt_16_0026.html"
date_collected: "2026-05-04"
category: "migration_tools"
original_path: "zh/mindstudio/830/T&ITools/MigrationTool/atlasfmkt_16_0026.html"
---

# 引用库找不到的问题

引用库找不到的问题，有可能是以下三种情况，请根据实际情况进行排查：

- 如果是当前目录或子目录中存在的文件夹或者文件，只需将该目录的父目录加到PYTHONPATH环境变量中即可。
- **如果找不到的引用库为requirements.txt中说明需要pip安装的包，可以使用pip install 包名**进行安装，若安装失败可以git clone安装包，使用python3 setup.py install安装。
- 检查找不到的引用库是否为readme.md中说明需要通过git clone下载安装的安装包，如果是，请按照要求下载并安装。
**父主题：**[FAQ](atlasfmkt_16_0024.html)