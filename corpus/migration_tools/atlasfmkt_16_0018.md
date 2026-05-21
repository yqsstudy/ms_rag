---
title: "迁移分析"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/MigrationTool/atlasfmkt_16_0018.html"
date_collected: "2026-05-04"
category: "migration_tools"
original_path: "zh/mindstudio/830/T&ITools/MigrationTool/atlasfmkt_16_0018.html"
---

# 迁移分析

PyTorch Analyse工具提供分析脚本，帮助用户在执行迁移操作前，分析基于GPU平台的PyTorch训练脚本中API、三方库套件、亲和API分析以及动态shape的支持情况，具体请参见表1。
**表1**分析模式介绍
分析模式

分析脚本

分析结果

调优建议

三方库套件分析模式

需用户提供待分析的三方库套件源码。

可快速获得源码中不支持的三方库API和CUDA信息。
说明：
三方库API是指在三方库代码中的函数，如果某函数的函数体内使用了不支持的torch算子或者CUDA自定义算子，则此函数就是三方库不支持的API。如果第三方库中其他函数调用了这些不支持的API，则这些调用函数也为不支持的API。

-

API支持情况分析模式

需用户提供待分析的PyTorch训练脚本。

可快速获得训练脚本中不支持的torch API和CUDA API信息。

输出训练脚本中API精度和性能调优的专家建议。

动态shape分析模式

可快速获得训练脚本中包含的动态shape信息。

-

亲和API分析模式

可快速获得训练脚本中可替换的亲和API信息。

-
|  |  |  |  |
| --- | --- | --- | --- |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |

#### 前提条件
**使用PyTorch Analyse工具前须安装如下依赖。如下命令若使用非root用户安装，需要在安装命令后加上--user****，例如：pip3 install pandas****--user**，安装命令可在任意路径下执行。
```
pip3 install pandas         #pandas版本号需大于或等于1.2.4
pip3 install libcst         #Python语法树解析器，用于解析Python文件
pip3 install prettytable    #将数据可视化为图表形式
pip3 install jedi           #三方库套件、亲和API分析时必须安装
```

#### 启动分析任务

1. 进入分析工具所在路径。

**
```
cd ${INSTALL_DIR}/cann/tools/ms_fmk_transplt/     #
${INSTALL_DIR}请替换为CANN软件安装后文件存储路径。以root用户安装为例，则安装后文件存储路径为：/usr/local/Ascend/cann。
```

2. 启动分析任务。

参考表2配置信息，执行如下命令启动分析任务。******************
```
./pytorch_analyse.sh -i /home/xxx/analysis -o /home/xxx/analysis_output -v 2.1.0 [-m torch_apis]    # /home/xxx/analysis为待分析脚本路径，/home/xxx/analysis_output为分析结果输出路径，2.1.0为待分析脚本框架版本，
torch_apis为分析模式
```

[其中“[]”表示可选参数，实际使用可不用添加。若“-m/--mode”参数指定的分析模式为dynamic_shape，分析任务完成后需参考训练配置](atlasfmkt_16_0022.html#ZH-CN_TOPIC_0000002536921483)对训练脚本进行修改，才能获取动态shape分析报告。
**表2**参数说明
参数

参数说明

取值示例

-i

--input

  - 待分析脚本文件所在文件夹或三方库套件源码所在文件夹路径。
  - 必选。

*/home/xxx*/analysis

-o

--output

  - 分析结果文件的输出路径。
  - *会在该路径下生成xxxx*_analysis文件夹。
  - 必选。
 
 说明：
用户需确保分析结果文件的输出路径在运行前存在，否则分析迁移工具会提示error。

*/home/xxx*/analysis_output

-v

--version

  - 待分析脚本或三方库套件源码的PyTorch版本。
  - 必选。

  - 1.11
  - 2.1.0
  - 2.2.0
  - 2.3.1
  - 2.4.0
  - 2.5.1
  - 2.6.0
 
 说明：
自动迁移方式的情况下，PyTorch 1.11.0版本不支持
 Atlas A3 训练系列产品
 /
 Atlas A3 推理系列产品
 。

-m

--mode

  - 分析的模式。目前支持torch_apis（API支持情况分析）、third_party（三方库套件分析）、affinity_apis（亲和API分析）和dynamic_shape（动态shape分析）模式。
  - 可选。

  - torch_apis（默认）
  - third_party
  - affinity_apis
  - dynamic_shape

-env

--env-path

  - 分析时需要增加的PYTHONPATH环境变量路径，仅安装jedi后该参数才生效。
  - 指定的三方库待分析的路径，分析当前脚本中不支持的三方库的API列表。
  - 可选。

/home/xxx/transformers/src /home/xxx/transformers/utils

多个文件路径使用空格隔开。

-api

--api-files

  - 三方库不支持API的分析结果文件。
  - 可选。
 
 说明：
若三方库存在不支持的API，且自定义函数调用了不支持的torch API，可使用分析torch API的功能。

    1. 使用-m中third_party（三方库套件分析）分析功能，获得三方库中不支持迁移的API列表（csv文件），示例如下：********
```
pytorch_analyse.sh -i third_party_input_path -o third_party_output_path -v 2.1.0 -m third_party # third_party_input_path为三方库文件夹路径，third_party_output_path为结果输出路径，2.1.0为待分析脚本框架版本
```

    2. 将上述步骤中获取的csv文件传入-api，获取当前训练脚本中不支持迁移的三方库API信息，示例如下：
```
pytorch_analyse.sh -i input_path -o output_path -v 2.1.0 -api third_party_output_path/framework_unsupported_op.csv   # input_path为模型脚本文件夹路径，output_path为结果输出路径，third_party_output_path/framework_unsupported_op.csv为步骤1中得到的三方库不支持api分析结果文件
```

/home/xxx/mmcv_analysis/full_unsupported_results.csv /home/xxx/transformers_analysis/full_unsupported_results.csv

多个文件路径使用空格隔开。

-h

--help

打印帮助信息。

-
|  |  |  |
| --- | --- | --- |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |

3. 分析完成后，进入脚本分析结果输出路径，查看分析报告，具体请参见分析报告简介。

#### 分析报告简介

- 分析模式为“torch_apis”时，分析结果如下所示：
```
1
2
3
4
5
6
7
```

```
├── xxxx_analysis     // 分析结果输出目录
│   ├── cuda_op_list.csv             //CUDA API列表
│   ├── unknown_api.csv              //支持存疑的API列表
│   ├── unsupported_api.csv          //不支持的API列表
│   ├── api_precision_advice.csv    //API精度调优的专家建议
│   ├── api_performance_advice.csv  //API性能调优的专家建议
│   ├── pytorch_analysis.txt         // 分析过程日志

```
|  |  |
| --- | --- |
**表3**“torch_apis”模式csv文件介绍
文件名

简介

unsupported_api.csv

[当前框架不支持的API列表，可以在昇腾开源社区](https://gitcode.com/Ascend/pytorch)寻求帮助。
**图1**
![](figure/zh-cn_image_0000002502718158.png "点击放大")不支持的API列表示例
cuda_op_list.csv

当前训练脚本包含的CUDA API信息。

unknown_api.csv

支持存疑的API列表，具体的PyTorch API信息请参见表4。

[如果训练失败，可以到昇腾开源社区](https://gitcode.com/Ascend/pytorch)求助。

api_precision_advice.csv

[当前训练脚本中可以进行精度调优的专家建议，除此之外，还可以使用《精度调试工具用户指南](https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/ModelAccuracyAnalyzer/atlasaccuracy_16_1000.html)》进行调优。

api_performance_advice.csv

[当前训练脚本中可以进行性能调优的专家建议和指导措施，除此之外，还可以使用《性能调优工具用户指南](https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0001.html)》进行调优。
说明：
分析结果基于原生PyTorch框架的API接口信息，具体请参见表4。
|  |  |
| --- | --- |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
**表4**PyTorch API接口信息
PyTorch框架版本

API信息参考链接

Ascend Extension for PyTorch版本

CANN版本

2.8.0

[PyTorch2.8.0](https://www.hiascend.com/document/detail/zh/Pytorch/720/apiref/PyTorchNativeapi/ptaoplist_000003.html)

[7.2.0](https://www.hiascend.com/developer/download/commercial/result?module=pt)

[商用版：8.3.RC1](https://www.hiascend.com/developer/download/commercial/result?module=pt)

[社区版：8.3.RC1](https://www.hiascend.com/developer/download/community/result?module=cann&cann=8.3.RC1)

2.7.1

[PyTorch2.7.1](https://www.hiascend.com/document/detail/zh/Pytorch/720/apiref/PyTorchNativeapi/ptaoplist_000078.html)

2.6.0

[PyTorch2.6.0](https://www.hiascend.com/document/detail/zh/Pytorch/710/apiref/PyTorchNativeapi/ptaoplist_000003.html)

[7.1.0](https://www.hiascend.com/developer/download/commercial/result?product=4&model=8&solution=c5b8ed4e2c804f70906a0cdffee12b9f)

[商用版：8.2.RC1](https://www.hiascend.com/developer/download/commercial/result?product=4&model=8&solution=c5b8ed4e2c804f70906a0cdffee12b9f)

[社区版：8.2.RC1](https://www.hiascend.com/developer/download/community/result?module=cann&cann=8.2.RC1)

2.5.1

[PyTorch2.5.1](https://www.hiascend.com/document/detail/zh/Pytorch/710/apiref/PyTorchNativeapi/ptaoplist_000077.html)

2.3.1

[PyTorch2.3.1](https://www.hiascend.com/document/detail/zh/Pytorch/710/apiref/PyTorchNativeapi/ptaoplist_000149.html)

2.5.1

[PyTorch2.5.1](https://www.hiascend.com/document/detail/zh/Pytorch/700/apiref/apilist/ptaoplist_000005.html)

[7.0.0](https://www.hiascend.com/developer/download/commercial/result?product=4&model=14&solution=95660a4d75cf44a49463373d356c1a78)

[商用版：8.1.RC1](https://www.hiascend.com/developer/download/commercial/result?product=4&model=8&solution=95660a4d75cf44a49463373d356c1a78)

[社区版：8.1.RC1](https://www.hiascend.com/developer/download/community/result?module=cann&cann=8.1.RC1)

2.4.0

[PyTorch2.4.0](https://www.hiascend.com/document/detail/zh/Pytorch/700/apiref/apilist/ptaoplist_000371.html)

2.3.1

[PyTorch2.3.1](https://www.hiascend.com/document/detail/zh/Pytorch/700/apiref/apilist/ptaoplist_000730.html)

2.1.0

[PyTorch2.1.0](https://www.hiascend.com/document/detail/zh/Pytorch/700/apiref/apilist/ptaoplist_001088.html)

2.1.0

[PyTorch 2.1.0](https://www.hiascend.com/document/detail/zh/Pytorch/600/apiref/apilist/ptaoplist_000704.html)

[6.0.0](https://www.hiascend.com/developer/download/commercial/result?product=4&model=14&solution=30612d961f7741b1a95f87775a9b2bcb)

[商用版：8.0.0](https://www.hiascend.com/developer/download/commercial/result?product=4&model=8&solution=30612d961f7741b1a95f87775a9b2bcb)

[社区版：8.0.0.beta1](https://www.hiascend.com/developer/download/community/result?module=cann&cann=8.0.0.beta1)

2.3.1

[PyTorch 2.3.1](https://www.hiascend.com/document/detail/zh/Pytorch/600/apiref/apilist/ptaoplist_000355.html)

2.4.0

[PyTorch 2.4.0](https://www.hiascend.com/document/detail/zh/Pytorch/600/apiref/apilist/ptaoplist_000005.html)

2.1.0

[PyTorch 2.1.0](https://www.hiascend.com/document/detail/zh/Pytorch/60RC3/apiref/apilist/ptaoplist_000701.html)

[6.0.rc3](https://www.hiascend.com/developer/download/commercial/result?product=4&model=14&solution=4f0929885dcb40a7a12be5704f5ccb15)

[商用版：8.0.RC3](https://www.hiascend.com/developer/download/commercial/result?product=4&model=8&solution=4f0929885dcb40a7a12be5704f5ccb15)

[社区版：8.0.RC3.beta1](https://www.hiascend.com/developer/download/community/result?module=cann&cann=8.0.RC3.beta1)

2.3.1

[PyTorch 2.3.1](https://www.hiascend.com/document/detail/zh/Pytorch/60RC3/apiref/apilist/ptaoplist_000315.html)

2.4.0

[PyTorch 2.4.0](https://www.hiascend.com/document/detail/zh/Pytorch/60RC3/apiref/apilist/ptaoplist_000005.html)

1.11.0

[PyTorch 1.11.0](https://www.hiascend.com/document/detail/zh/Pytorch/60RC2/apiref/apilist/ptaoplist_001028.html)

[6.0.rc2](https://www.hiascend.com/developer/download/commercial/result?product=4&model=14&solution=e61cfe776f1f4a84925d853055ee059c)

[商用版：8.0.RC2](https://www.hiascend.com/developer/download/commercial/result?product=4&model=8&solution=e61cfe776f1f4a84925d853055ee059c)

[社区版：8.0.RC2.beta1](https://www.hiascend.com/developer/download/community/result?module=cann&cann=8.0.RC2.beta1)

2.1.0

[PyTorch 2.1.0](https://www.hiascend.com/document/detail/zh/Pytorch/60RC2/apiref/apilist/ptaoplist_000647.html)

2.2.0

[PyTorch 2.2.0](https://www.hiascend.com/document/detail/zh/Pytorch/60RC2/apiref/apilist/ptaoplist_000326.html)

2.3.1

[PyTorch 2.3.1](https://www.hiascend.com/document/detail/zh/Pytorch/60RC2/apiref/apilist/ptaoplist_000004.html)

1.11.0

[PyTorch 1.11.0](https://www.hiascend.com/document/detail/zh/Pytorch/60RC1/apiref/apilist/ptaoplist_000625.html)

[6.0.rc1](https://www.hiascend.com/developer/download/commercial/result?product=4&model=14&solution=3b6d40b14b96433a8c5e40ed08e4b83e)

[商用版：8.0.RC1](https://www.hiascend.com/developer/download/commercial/result?product=4&model=8&solution=3b6d40b14b96433a8c5e40ed08e4b83e)

[社区版：8.0.RC1.beta1](https://www.hiascend.com/developer/download/community/result?module=cann&cann=8.0.RC1.beta1)

2.1.0

[PyTorch 2.1.0](https://www.hiascend.com/document/detail/zh/Pytorch/60RC1/apiref/apilist/ptaoplist_000313.html)

2.2.0

[PyTorch 2.2.0](https://www.hiascend.com/document/detail/zh/Pytorch/60RC1/apiref/apilist/ptaoplist_000005.html)
|  |  |  |  |
| --- | --- | --- | --- |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |

- 分析模式为“third_party”时，分析结果如下所示：
```
1
2
3
4
5
6
7
```

```
├── xxxx_analysis     // 分析结果输出目录
│   ├── cuda_op.csv                  //CUDA API列表
│   ├── framework_unsupported_op.csv //框架不支持的API列表
│   ├── full_unsupported_results.csv //全量不支持的API列表
│   ├── migration_needed_op.csv      //待迁移的API列表
│   ├── unknown_op.csv              //支持情况存疑的API列表
│   ├── pytorch_analysis.txt         // 分析过程日志

```
|  |  |
| --- | --- |
**表5**“third_party”模式csv文件介绍
文件名

简介

framework_unsupported_op.csv

[框架不支持的API列表，查看三方库源码中当前框架不支持的三方库API。对于当前框架不支持的API，可以到昇腾开源社区](https://gitcode.com/Ascend/pytorch)求助。
**图2**
![](figure/zh-cn_image_0000002502718160.png "点击放大")框架不支持的API列表示例
cuda_op.csv

当前三方库源码包含的CUDA API信息。

full_unsupported_results.csv

全量不支持的API列表，由于不支持CUDA和PyTorch框架而导致不支持第三方库的API列表。可以在其他调用已分析三方库源码的训练脚本执行分析操作时，使用“-api”指定，帮助用户快速获得分析结果。

migration_needed_op.csv

待迁移的API列表，列表中的API支持使用迁移工具进行迁移。

unknown_op.csv

[支持情况存疑的API列表。如果训练失败，可以到昇腾开源社区](https://gitcode.com/Ascend/pytorch)求助。
|  |  |
| --- | --- |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |

- 分析模式为“affinity_apis”时，分析结果如下所示：
```
1
2
3
```

```
├── xxxx_analysis // 分析结果输出目录
│   ├──  affinity_api_call.csv      // 可替换为亲和API的原生API调用列表
│   ├──  pytorch_analysis.txt       // 分析过程日志

```
|  |  |
| --- | --- |
**分析报告affinity_api_call.csv包括原生API的调用信息，并将其分为几种类型：class（类）、function（方法）、torch（Pytorch框架API）以及special（特殊表达式）。用户可以根据分析报告，在训练脚本中将原生API手动替换为指定的亲和API，替换后的脚本在昇腾AI处理器上运行时，性能更优。分析报告示例如下。
 
 图3**
![](figure/zh-cn_image_0000002534478197.png "点击放大")亲和API分析报告示例
- 分析模式为“dynamic_shape”时，分析结果如下所示：
```
1
2
3
4
5
```

```
├── xxxx_analysis     // 分析结果输出目录
│   ├── 生成脚本文件                 // 与分析前的脚本文件目录结构一致
│   ├── msft_dynamic_analysis
│         ├── hook.py         //包含动态shape分析的功能参数
│         ├── __init__.py

```
|  |  |
| --- | --- |

生成动态shape分析结果件后，还需要先修改分析结果输出目录下训练脚本文件中的读取训练数据集的for循环，手动开启动态shape检测，请参考下方示例进行修改。
修改前：
```
for i, (ings, targets, paths, _) in pbar:
```

修改如下加粗字体信息：
************
```
for i, (ings, targets, paths, _) in DETECTOR.start(pbar):
```

运行分析修改后的训练脚本，将在分析结果件所在的根目录下生成保存动态shape的分析报告msft_dynamic_shape_analysis_report.csv。

  - 动态shape分析得到的模型训练脚本文件建议在GPU上执行。若已完成模型训练脚本文件迁移且需要在NPU上运行时，则存在动态shape的算子运行时间将会较长。
  - 若生成的msft_dynamic_shape_analysis_report.csv文件内容为空时，表示训练脚本中没使用动态shape。