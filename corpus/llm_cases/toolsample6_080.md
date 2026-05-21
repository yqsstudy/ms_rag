---
title: "异常堆栈捕获"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_080.html"
date_collected: "2026-05-04"
category: "llm_cases"
original_path: "zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_080.html"
---

# 异常堆栈捕获

当检测到性能异常时，需及时捕获并分析相关堆栈信息：

- **gdb 查看**
```
gdb -p <pid>
#进入GDB命令行，打印进程/主线程调用栈
bt
#查看线程调用栈
info threads
thread<n>
bt
```

- **pstack 查看**
```
pstack <pid>
```

- **cat 查看**
```
cat /proc/<pid>/stack
```

**父主题：**[正式分析](toolsample6_078.html)