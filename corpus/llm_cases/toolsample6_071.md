---
title: "前置准备"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_071.html"
date_collected: "2026-05-04"
category: "llm_cases"
original_path: "zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_071.html"
---

# 前置准备

```
# 下载torch源码，以2.1.0版本为例
git clone -b v2.1.0 https://github.com/pytorch/pytorch.git pytorch-2.1.0
cd pytorch-2.1.0
git submodule sync
git submodule update --init --recursive

# 安装torch依赖
pip install -r requirements.txt

#下载torch_npu源码，要求和torch版本对应
git clone -b v2.1.0 https://gitee.com/ascend/pytorch.git torch_npu
```

需修改torch源码目录下的CMakeLists.txt文件，注释以下行以屏蔽告警（torch高版本已移除该行，无需注释）：

```
append_cxx_flag_if_supported("-Werror=cast-function-type" CMAKE_CXX_FLAGS)
```
**图1**
**代码注释示意

父主题：**[torch及torch_npu编译优化](toolsample6_070.html)