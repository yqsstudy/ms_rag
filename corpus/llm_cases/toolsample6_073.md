---
title: "采集Profiling数据"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_073.html"
date_collected: "2026-05-04"
category: "llm_cases"
original_path: "zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_073.html"
---

# 采集Profiling数据

```
# 安装插桩包
pip install pytorch-2.1.0/dist/torch-*.whl --force-reinstall --no-deps
pip install torch_npu/dist/torch_npu-*.whl --force-reinstall --no-deps

# 设置关键环境变量
export OMP_PROC_BIND=false
export LLVM_PROFILE_FILE=/tmp/profile/default_%m.profraw  # 确保/tmp/profile目录为空

# 执行实际训练任务采集性能数据，例如: bash run_model.sh
...
```
**父主题：**[torch及torch_npu编译优化](toolsample6_070.html)