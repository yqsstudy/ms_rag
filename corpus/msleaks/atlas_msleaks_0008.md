---
title: "mstx打点采集"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/msleaks/atlas_msleaks_0008.html"
date_collected: "2026-05-04"
category: "msleaks"
original_path: "zh/mindstudio/830/T&ITools/msleaks/atlas_msleaks_0008.html"
---

# mstx打点采集

msLeaks工具可以结合mstx打点能力进行内存采集和Host侧内存采集，同时msLeaks工具能够在可视化Trace中标记打点位置，便于用户定位问题代码行。

[对于C脚本和Python脚本，mstx打点方式略有不同，可参考《MindStudio mstx API参考](https://www.hiascend.com/document/detail/zh/mindstudio/830/API/mstxAPIReference/msprof_tx_0001.html)》。

*开启msLeaks工具的Host侧内存采集功能后，输出的leaks_dump_{timestamp**}.csv文件中会存在大量Host侧malloc/free记录，cpu_**trace_{timestamp*}.json文件中也会存在Host侧内存相关信息。

下方以Python脚本示例，展示mstx结合msLeaks工具进行内存分析。

- 内存分析请在训练推理脚本内的Step开始和结束处进行标记，并使用固化信息“step start”标识Step开始，示例如下：
```
1
2
3
4
5
6
```

```
import mstx
for epoch in range(15): 
    id = mstx.range_start("step start", None) # 标识Step开始并开启内存分析功能
    ....
    ....
    mstx.range_end(id)  # 标识Step结束

```
|  |  |
| --- | --- |

- Host侧内存采集
由于采集整个进程的Host侧内存，会出现落盘文件数据量大、难以解析的情况，因此我们选择通过标识来开启和关闭采集，在所需的Host侧内存操作的代码段前后添加mstx打点，并使用固化信息“report host memory info start”，示例如下：

```
1
2
3
4
5
```

```
import mstx
id = mstx.range_start("report host memory info start", None)
...
...
mstx.range_end(id)  # 标识停止采集Host侧内存操作

```
|  |  |
| --- | --- |


- 仅支持采集单卡局部的内存数据。
- 在需要的用户程序前可添加PYTHONMALLOC=malloc。
PYTHONMALLOC=malloc是Python的环境变量，表示不采用Python的默认内存分配器，所有的内存分配均使用malloc，该配置对小内存申请有一定影响。

- 在MindStudio下一个版本中，将不再支持Host侧内存采集功能。
**父主题：**[内存采集](atlas_msleaks_0003.html)