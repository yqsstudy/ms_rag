---
title: "编译优化包获取"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_063.html"
date_collected: "2026-05-04"
category: "llm_cases"
original_path: "zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_063.html"
---

# 编译优化包获取

[编译优化环境配置复杂，完整流程耗时较长，为提升部署效率，实现开箱即用的性能收益，用户可直接获取预构建的泛化编译优化包，包含Python编译优化后的压缩包，以及torch、torch_npu的whl安装包。Python压缩包可以直接配置软连接](https://repo.oepkgs.net/ascend/pytorch/vllm/python/)使用，torch、torch_npu的whl安装包则是基于典型场景的模型数据优化生成，具有一定泛化性能收益，软件包获取链接请参见表1。
**表1**vLLM场景软件包获取
名称

获取链接

Python压缩包

[https://repo.oepkgs.net/ascend/pytorch/vllm/python/](https://repo.oepkgs.net/ascend/pytorch/vllm/python/)

torch、torch_npu whl安装包

[https://repo.oepkgs.net/ascend/pytorch/vllm/torch/](https://repo.oepkgs.net/ascend/pytorch/vllm/torch/)

运行时依赖so

[https://repo.oepkgs.net/ascend/pytorch/vllm/lib/](https://repo.oepkgs.net/ascend/pytorch/vllm/lib/)
|  |  |
| --- | --- |
|  |  |
|  |  |
|  |  |
**父主题：**[编译优化](toolsample6_062.html)