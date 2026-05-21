---
title: "注意事项"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_069.html"
date_collected: "2026-05-04"
category: "llm_cases"
original_path: "zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_069.html"
---

# 注意事项

- 若模型运行时提示.so文件或模块缺失，需检查依赖是否安装完整。
- 编译完成的Python环境可跨服务器迁移，但需注意仅支持从低版本glibc环境向高版本迁移，反向迁移不可行。
**父主题：**[Python编译优化](toolsample6_065.html)