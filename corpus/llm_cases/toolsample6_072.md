---
title: "首次编译（插桩编译）"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_072.html"
date_collected: "2026-05-04"
category: "llm_cases"
original_path: "zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_072.html"
---

# 首次编译（插桩编译）

```
# 配置环境变量（/path/to/profile为默认的性能数据存储路径，后续可通过设置LLVM_PROFILE_FILE修改）
export CMAKE_C_FLAGS="-flto=thin -fuse-ld=lld -fprofile-generate=/path/to/profile"
export CMAKE_CXX_FLAGS="-flto=thin -fuse-ld=lld -fprofile-generate=/path/to/profile"
export CC=clang
export CXX=clang++
export USE_XNNPACK=0

# 编译torch
cd pytorch-2.1.0
git clean -dfx
python3 setup.py bdist_wheel

# 编译torch_npu（需先安装新编译的torch）
cd torch_npu
git clean -dfx
bash ci/build.sh --python=3.8 --enable_lto --enable_pgo=1
```
**父主题：**[torch及torch_npu编译优化](toolsample6_070.html)