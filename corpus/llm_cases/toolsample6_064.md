---
title: "毕昇编译器安装"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_064.html"
date_collected: "2026-05-04"
category: "llm_cases"
original_path: "zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_064.html"
---

# 毕昇编译器安装

Python编译优化以及torch、torch_npu的编译优化均需预先安装毕昇编译器。

1. [请从鲲鹏社区官网获取该编译器的安装包。以4.1.0版本为例，单击获取链接](https://kunpeng-repo.obs.cn-north-4.myhuaweicloud.com/BiSheng Enterprise/BiSheng Enterprise 203.0.0/BiShengCompiler-4.1.0-aarch64-linux.tar.gz)下载。
2. 下载后执行以下安装及配置命令。

```
# 解压毕昇编译器安装包
tar -xvf BiShengCompiler-4.1.0-aarch64-linux.tar.gz

# 配置环境变量
export PATH=$(pwd)/BiShengCompiler-4.1.0-aarch64-linux/bin:$PATH
export LD_LIBRARY_PATH=$(pwd)/BiShengCompiler-4.1.0-aarch64-linux/lib:$LD_LIBRARY_PATH
```

3. 配置完成后，执行以下命令验证安装。

```
clang -v
```

4. 若显示如下版本信息，则表明配置成功。
**图1**
毕昇编译器配置成功打印信息

**父主题：**[编译优化](toolsample6_062.html)