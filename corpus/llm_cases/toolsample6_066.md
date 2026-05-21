---
title: "安装依赖"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_066.html"
date_collected: "2026-05-04"
category: "llm_cases"
original_path: "zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_066.html"
---

# 安装依赖

Python源码编译过程会尝试调用系统库。若编译时相关系统头文件缺失，虽可完成编译，但运行时调用到相应组件将触发错误。

- **Fedora/RHEL/CentOS (dnf-based系统)**:
```
sudo dnf install gcc gcc-c++ gdb lzma glibc-devel libstdc++-devel openssl-devel \
readline-devel zlib-devel libffi-devel bzip2-devel xz-devel \
sqlite sqlite-devel sqlite-libs libuuid-devel gdbm-libs perf \
expat expat-devel mpdecimal python3-pip
```

- **Debian/Ubuntu (apt-based系统)**:
```
sudo apt-get install build-essential gdb lcov pkg-config \
libbz2-dev libffi-dev libgdbm-dev libgdbm-compat-dev liblzma-dev \
libncurses5-dev libreadline6-dev libsqlite3-dev libssl-dev \
lzma lzma-dev tk-dev uuid-dev zlib1g-dev libmpdec-dev
```

**父主题：**[Python编译优化](toolsample6_065.html)