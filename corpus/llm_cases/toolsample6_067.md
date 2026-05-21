---
title: "编译Python"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_067.html"
date_collected: "2026-05-04"
category: "llm_cases"
original_path: "zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_067.html"
---

# 编译Python

[根据需求从以下地址下载对应版本的Python源码并解压：https://www.python.org/downloads/source/](https://www.python.org/downloads/source/)。

以Python 3.8.17为例，参考以下命令编译安装。

```
# 解压源码文件并进入目录
tar -xvf Python-3.8.17.tgz
cd Python-3.8.17

# 配置编译环境（需预装毕昇编译器）
export CC=clang
export CXX=clang++

# 编译安装（<install_path>为Python安装目标绝对路径）
mkdir -p <install_path>
./configure --prefix=<install_path> --with-lto --enable-optimizations
make -j
make install
```

编译完成后，<install_path>/bin目录下将生成带有编译优化效果的python3及pip3可执行文件。
**父主题：**[Python编译优化](toolsample6_065.html)