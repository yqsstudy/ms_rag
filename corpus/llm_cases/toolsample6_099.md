---
title: "AOE调优"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_099.html"
date_collected: "2026-05-04"
category: "llm_cases"
original_path: "zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_099.html"
---

# AOE调优

对于EP模式的产品，可以直接在OM模型运行的环境进行AOE调优。参考命令如下：

```
aoe --framework 5 --model ./model.onnx --output model --job_type 2 --ip xx.xx.xx.xx --aicore_num=1
```

[参数的详细解释以及使用方法可参见《AOE调优工具用户指南](https://www.hiascend.com/document/detail/zh/canncommercial/850/devaids/aoe/auxiliarydevtool_aoe_0001.html)》。
**父主题：**[ONNX模型调优](toolsample6_096.html)