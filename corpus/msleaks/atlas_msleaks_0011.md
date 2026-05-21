---
title: "Python Trace采集"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/msleaks/atlas_msleaks_0011.html"
date_collected: "2026-05-04"
category: "msleaks"
original_path: "zh/mindstudio/830/T&ITools/msleaks/atlas_msleaks_0011.html"
---

# Python Trace采集

msLeaks工具支持通过Python接口采集Python代码的Trace数据，并与内存事件使用统一时间轴，帮助调优人员快速关联内存事件与全链路代码，精准定位问题。

#### 操作步骤

1. 在msLeaks工具中，增加Python接口，用以开启和关闭Tracer功能，在start和stop之间的Python代码，会落盘Trace数据。
代码示例如下：
```
1
2
3
4
5
```

```
import msleaks

msleaks.tracer.start()  # 开启Tracer功能 
train()                 # train()为用户代码
msleaks.tracer.stop()   # 关闭Tracer功能

```
|  |  |
| --- | --- |

2. *执行完成后，会生成名称为python_trace_{TID**}_{timestamp*[}.csv的文件，具体文件信息可参见输出说明](atlas_msleaks_0016.html#ZH-CN_TOPIC_0000002506628524)。
**父主题：**[内存采集](atlas_msleaks_0003.html)