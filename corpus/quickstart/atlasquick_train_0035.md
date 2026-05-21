---
title: "使用MindStudio Insight工具可视化性能数据"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/msquickstart/atlasquick_train_0035.html"
date_collected: "2026-05-04"
category: "quickstart"
original_path: "zh/mindstudio/830/msquickstart/atlasquick_train_0035.html"
---

# 使用MindStudio Insight工具可视化性能数据

- [性能数据采集](atlasquick_train_0032.html)生成的性能数据均可以使用MindStudio Insight工具将性能数据可视化。
- [执行msprof-analyze分析](atlasquick_train_0034.html#ZH-CN_TOPIC_0000002534411973__section1338013333519)时，输出的交付件需要使用MindStudio Insight工具将数据可视化。

#### 前提条件

[完成性能数据采集](atlasquick_train_0032.html)[或执行msprof-analyze分析](atlasquick_train_0034.html#ZH-CN_TOPIC_0000002534411973__section1338013333519)，获取对应交付件。

#### 操作步骤

1. 安装MindStudio Insight。
[参见《MindStudio Insight工具用户指南](https://www.hiascend.com/document/detail/zh/mindstudio/830/GUI_baseddevelopmenttool/msascendinsightug/Insight_userguide_0002.html)[》中的“安装与卸载](https://www.hiascend.com/document/detail/zh/mindstudio/830/GUI_baseddevelopmenttool/msascendinsightug/Insight_userguide_0005.html)”章节下载并安装MindStudio Insight。

MindStudio Insight可视化工具推荐在Windows环境使用。

2. 双击桌面的MindStudio Insight快捷方式图标，启动MindStudio Insight。
3. 导入性能数据。
  1. [将性能数据采集](atlasquick_train_0032.html)[或执行msprof-analyze分析](atlasquick_train_0034.html#ZH-CN_TOPIC_0000002534411973__section1338013333519)的性能数据拷贝至Windows环境。
  2. **单击MindStudio Insight界面左上方“导入数据”，在弹框中选择性能数据文件或目录，然后单击“确认”进行导入，如下所示。图1**
**导入性能数据
图2**
展示性能数据

4. 分析性能数据。
[MindStudio Insight工具将性能数据可视化后可以更直观地分析性能瓶颈，详细分析方法请参见《MindStudio Insight工具用户指南](https://www.hiascend.com/document/detail/zh/mindstudio/830/GUI_baseddevelopmenttool/msascendinsightug/Insight_userguide_0002.html)》。

**父主题：**[性能数据分析](atlasquick_train_0033.html)