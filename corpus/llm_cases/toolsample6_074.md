---
title: "二次编译（优化编译）"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_074.html"
date_collected: "2026-05-04"
category: "llm_cases"
original_path: "zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_074.html"
---

# 二次编译（优化编译）

```
# 转换Profiling数据格式
llvm-profdata merge /tmp/profile -o default.profdata

# 配置优化编译环境
export CMAKE_C_FLAGS="-flto=thin -fuse-ld=lld -fprofile-use=/path/to/profile/default.profdata"
export CMAKE_CXX_FLAGS="-flto=thin -fuse-ld=lld -fprofile-use=/path/to/profile/default.profdata"
export CC=clang
export CXX=clang++
export USE_XNNPACK=0

# 编译优化版torch
cd pytorch-2.1.0
git clean -dfx
python3 setup.py bdist_wheel

# 编译优化版torch_npu（需复制default.profdata至torch_npu目录）
cd torch_npu
git clean -dfx
cp /path/to/profile/default.profdata .
bash ci/build.sh --python=3.8 --enable_lto --enable_pgo=2
```

编译生成的torch及torch_npu即为高性能优化包。
**父主题：**[torch及torch_npu编译优化](toolsample6_070.html)