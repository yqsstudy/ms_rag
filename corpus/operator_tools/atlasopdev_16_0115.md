---
title: "mstx扩展功能"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0115.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0115.html"
---

# mstx扩展功能

#### mstx接口简介

mstx接口是MindStudio提供的一个性能分析接口，它允许用户在应用程序中插入特定的标记，以便在性能分析时能够更精确地定位关键代码区域，具体接口明细请参见表1和表2[。具体接口的使用情况请参考《MindStudio mstx API参考](https://www.hiascend.com/document/detail/zh/mindstudio/830/API/mstxAPIReference/msprof_tx_0001.html)》。
**表1**C/C++ mstx接口列表
接口名称

接口说明

msProf工具支持情况

mstxRangeStartA

mstx range指定范围能力的起始位置标记。

支持。

mstxRangeEnd

mstx range指定范围能力的结束位置标记。

支持。
|  |  |  |
| --- | --- | --- |
|  |  |  |
|  |  |  |
**表2**Python mstx接口列表
接口名称

接口说明

msProf工具支持情况

mstx.range_start

mstx range指定范围能力的起始位置标记。

支持。

mstx.range_end

mstx range指定范围能力的结束位置标记。

支持。
|  |  |  |
| --- | --- | --- |
|  |  |  |
|  |  |  |

#### mstx接口的使用

- msProf工具允许用户通过mstx接口实现特定算子调优的功能，使用mstx接口可以自定义采集代码段范围内或指定关键函数的开始和结束时间点，并识别关键函数或计算API等信息，对性能问题快速定界。
- [默认情况下mstx接口不使能。若用户在应用程序中调用mstx接口，工具会根据具体使用场景使能mstx打点功能。例如配置--mstx=on使能用户程序中的mstx API，并可以通过--mstx-include使能用户程序中特定的mstx API，具体请参见命令汇总](atlasopdev_16_0082.html#ZH-CN_TOPIC_0000002505040624__zh-cn_topic_0000002534506413_section66278453613)中的--mstx和--mstx-include参数。
- [mstx当前提供了两种API的使用方式：库文件和头文件，以Link](https://gitee.com/ascend/samples/tree/master/operator/ascendc/0_introduction/1_add_frameworklaunch/AclNNInvocation)为例：
  - 此样例工程不支持Atlas A3 训练系列产品。

  - 在${git_clone_path}/samples/operator/ascendc/0_introduction/1_add_frameworklaunch/AclNNInvocation/src/CMakeLists.txt路径下新增库文件libms_tools_ext.so，地址为：${INSTALL_DIR}/lib64/libms_tools_ext.so。********
```
# Header path
include_directories(
     ...
    ${CUST_PKG_PATH}/include
)
...
target_link_libraries( 
    ...
    dl
)
```

  - 在${git_clone_path}/samples/operator/ascendc/0_introduction/1_add_frameworklaunch/AclNNInvocation/src/main.cpp路径下，将用户程序编译链接dl库，对应的头文件ms_tools_ext.h地址：${INSTALL_DIR}/include/mstx。****
```
...
#include "mstx/ms_tools_ext.h"
...
```

${INSTALL_DIR}请替换为CANN软件安装后文件存储路径。以root用户安装为例，则安装后文件存储路径为：/usr/local/Ascend/cann。

#### 调用示例

启动msProf工具后，执行msprof op --mstx=on --mstx-include=range1 --launch-count=2 python cal.py命令，将会采集range1范围内的算子，即sub和mul算子。

```
import mstx
import torch
import torch_npu
x = torch.Tensor([1,2,3,4]).npu()
y = torch.Tensor([1,2,3,4]).npu()
a = x + y
range1_id = mstx.range_start("range1", None)
b = a - x
c = a * x
mstx.range_end(range1_id)
f = x + e
range2_id = mstx.range_start("range2", None)
e = torch.abs(y)
mstx.range_end(range2_id)
```
**父主题：**[算子调优（msProf）](atlasopdev_16_0081.html)