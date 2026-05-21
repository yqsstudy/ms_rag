---
title: "工具概述"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0018.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0018.html"
---

# 工具概述

#### 工具概述

完成算子分析&原型定义后，可使用算子工程工具（msOpGen，MindStudio Ops Generator）生成自定义算子工程，并进行编译部署，具体流程请参考图1。

[在TBE及AI CPU算子开发场景中，msOpGen工具的使用详情请参考基于msOpGen工具创建算子工程](atlasopdev_10_0024.html#ZH-CN_TOPIC_0000002505040670)[及算子编译部署](atlasopdev_10_0087.html#ZH-CN_TOPIC_0000002536800627)。由于TBE/TIK算子开发方式已不再对外开放，TBE/TIK Sample将于MindStudio下个版本下线。

具有如下功能：

- 基于算子原型定义输出算子工程。
- 基于性能仿真环境生成的dump数据文件输出算子仿真流水图文件。
**图1**
![](figure/zh-cn_image_0000002502746532.png "点击放大")msOpGen工具使用流程介绍
#### 工具特性

msOpGen目前已支持的功能如下：包括算子工程创建、算子实现（Host侧&Kernel侧）、算子工程编译部署以及解析算子仿真流水图文件等。
**表1**msOpGen工具功能
功能

链接

算子工程创建

[创建算子工程](atlasopdev_16_0021.html#ZH-CN_TOPIC_0000002505040538)

算子实现（Host侧&Kernel侧）

[算子开发](atlasopdev_16_0023.html#ZH-CN_TOPIC_0000002536920467)

算子工程编译部署

[算子编译部署](atlasopdev_16_0024.html#ZH-CN_TOPIC_0000002504880720)

解析算子仿真流水图文件

[查看算子仿真流水图](atlasopdev_16_0025.html#ZH-CN_TOPIC_0000002505040542)
|  |  |
| --- | --- |
|  |  |
|  |  |
|  |  |
|  |  |

#### 命令汇总
执行如下命令，参数说明请参见表2。
用户按照输入的配置参数生成算子模板后，建议在运行前确认算子工程代码的安全性。
********
```
msopgen gen -i {*.json} -f {framework type} -c {Compute Resource} -lan cpp -out {Output Path}
```
**表2**创建算子工程参数说明
参数名称

参数描述

是否必选

gen

用于生成算子开发交付件。

是

-i，--input

**算子原型定义文件（.json**）路径，可配置为绝对路径或者相对路径。工具执行用户需要有此路径的可读权限。

是

-f，--framework

框架类型。

- 默认为TensorFlow框架，默认值：tf或者tensorflow
- Caffe框架，参数值：caffe
 
 说明：
自定义Ascend C算子不支持Caffe框架。

- PyTorch框架，参数值：pytorch
- MindSpore框架，参数值：ms或mindspore
- ONNX框架，参数值：onnx
说明：
- 所有参数值大小写不敏感。
- TBE&TIK不支持单算子API调用，默认生成TensorFlow框架。
- Ascend C算子工程支持TensorFlow框架、PyTorch框架和单算子API调用，默认生成TensorFlow框架。
- 当用户使用-f aclnn时，生成Ascend C简易算子工程，否则保持原功能特性生成。

否

-lan，--language

算子编码语言。

- cpp：基于Ascend C编程框架，使用C/C++编程语言进行开发。
- py：基于DSL和TIK算子编程框架，使用Python编程语言进行开发。

默认值：py。
说明：
**cpp**仅适用于Ascend C算子开发场景。

否

-c，--compute_unit

- 算子使用的计算资源。
*配置格式为：ai_core-{soc version}**，ai_core与{soc version}*之间用中划线“-”连接。

请根据实际昇腾AI处理器版本进行选择。

说明：
*AI处理器的型号<soc_version>*请通过如下方式获取：

- **非
 Atlas A3 训练系列产品
 /
 Atlas A3 推理系列产品
 ：在安装昇腾AI处理器的服务器执行npu-smi info****命令进行查询，获取Chip Name****信息。实际配置值为AscendChip Name，例如Chip Name***取值为xxxyy**，实际配置值为Ascendxxxyy**。当Ascendxxxyy为代码样例的路径时，需要配置ascendxxxyy*。
- **Atlas A3 训练系列产品
 /
 Atlas A3 推理系列产品
 ：在安装昇腾AI处理器的服务器执行npu-smi info -t board -i***id***-c***chip_id***命令进行查询，获取Chip Name****和NPU Name****信息，实际配置值为Chip Name_NPU Name。例如Chip Name***取值为Ascendxxx***，NPU Name***取值为1234，实际配置值为Ascendxxx**_**1234。当Ascendxxx**_**1234为代码样例的路径时，需要配置ascendxxx**_*1234。
其中：

  - **id：设备id，通过npu-smi info -l**命令查出的NPU ID即为设备id。
  - **chip_id：芯片id，通过npu-smi info -m**命令查出的Chip ID即为芯片id。

基于同系列的AI处理器型号创建的算子工程，其基础功能（基于该工程进行算子开发、编译和部署）通用。

- 针对AI CPU算子，请配置为：aicpu。
 
 说明：
在
 Atlas A3 训练系列产品
 /
 Atlas A3 推理系列产品
 场景下，请勿在编译时使用以下编译选项，否则会导致机器异常。

  - -march=armv8-a+lse
  - -march=armv8.1-a
  - -march=armv8.2-a
  - -march=armv8.3-a

是

-out，--output

生成文件所在路径，可配置为绝对路径或者相对路径，并且工具执行用户具有可读写权限。

若不配置，则默认生成在执行命令的当前路径。
说明：
若用户指定的输出目录中存在与模板工程重名的文件，输出目录中的文件将会被模板工程的文件覆盖。

否

-m，--mode

生成交付件模式。

- 0：创建新的算子工程，若指定的路径下已存在算子工程，则会报错退出。
- 1：在已有的算子工程中追加算子。

默认值：0。

否

-op，--operator

配置算子的类型，如：Conv2DTik。

若不配置此参数，当算子原型定义文件中存在多个算子时，工具会提示用户选择算子。

否

-h，--help

输出帮助信息。

否
|  |  |  |
| --- | --- | --- |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |

#### 补充说明

msOpGen工具其他参数说明可参考表3。
**表3**参数说明
参数名称

参数描述

说明

compile

编译TBE&AI CPU算子工程时使用。

[具体请参见算子交付件独立编译](atlasopdev_10_0090.html#ZH-CN_TOPIC_0000002505040674)
|  |  |  |
| --- | --- | --- |
|  |  |  |
**父主题：**[算子工程创建（msOpGen）](atlasopdev_16_0017.html)