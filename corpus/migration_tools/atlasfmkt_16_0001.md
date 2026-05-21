---
title: "工具简介"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/MigrationTool/atlasfmkt_16_0001.html"
date_collected: "2026-05-04"
category: "migration_tools"
original_path: "zh/mindstudio/830/T&ITools/MigrationTool/atlasfmkt_16_0001.html"
---

# 工具简介

昇腾NPU是AI算力的后起之秀，但目前训练和在线推理脚本大多是基于GPU的。由于NPU与GPU的架构差异，基于GPU的训练和在线推理脚本不能直接在NPU上使用。

分析迁移工具提供PyTorch训练脚本一键式迁移至昇腾NPU的功能，开发者可做到少量代码修改或零代码完成迁移。该工具提供PyTorch Analyse功能，帮助用户分析PyTorch训练脚本的API、三方库API、亲和API分析以及动态shape的支持情况。同时提供了自动迁移和PyTorch GPU2Ascend工具两种迁移方式，将基于GPU的脚本迁移为基于NPU的脚本，这种自动化方法节省了人工手动进行脚本迁移的学习成本与工作量，大幅提升了迁移效率。

- （推荐）自动迁移：修改内容少，只需在训练脚本中导入库代码，迁移后直接在昇腾NPU平台上运行。
- PyTorch GPU2Ascend工具迁移：迁移过程会生成分析文件，支持用户查看API支持度分析报告和迁移过程中对原训练脚本的修改内容，并支持单卡脚本迁移为多卡脚本。

使用分析迁移工具迁移前，请用户自行确认原工程内各参数的正确性，需在原工程运行成功的基础上使用工具进行迁移。