---
title: "准备模型文件和量化信息文件"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/ModelAccuracyAnalyzer/atlasaccuracy_16_0030.html"
date_collected: "2026-05-04"
category: "accuracy_tools"
original_path: "zh/mindstudio/830/T&ITools/ModelAccuracyAnalyzer/atlasaccuracy_16_0030.html"
---

# 准备模型文件和量化信息文件

#### 全网层信息文件

[以下介绍通过ATC模型转换工具获取离线模型的操作步骤，更多操作请参见《ATC离线模型编译工具用户指南](https://www.hiascend.com/document/detail/zh/canncommercial/850/devaids/atctool/atlasatc_16_0031.html)》。

1. 以运行用户登录Ascend-cann-toolkit所在环境。
2. 获取原始模型文件并保存在任意目录下。

例如：resnet50.prototxt和resnet50.caffemodel

3. 执行ATC模型转换。
**********
```
atc --model=$HOME/module/resnet50.prototxt --weight=$HOME/module/resnet50.caffemodel --framework=0 --output=$HOME/module/out/caffe_resnet50 --soc_version=<soc_version> 
```
若提示如下信息，则说明模型转换成功。
```
1
```

```
ATC run success

```
|  |  |
| --- | --- |

成功执行命令后，在--output参数指定的路径下，可查看离线模型（如：resnet50.om）。

4. 生成json文件。
******
```
atc --mode=1 --om=$HOME/module/out/caffe_resnet50/resnet50.om --json=$HOME/data/resnet50.json
```

若提示如下信息，则说明转换json文件成功。

```
1
```

```
ATC run success

```
|  |  |
| --- | --- |

成功执行命令后，在--json参数指定的路径下可查看转换后的json文件。

#### 量化原始模型和量化信息文件

[请参见《AMCT模型压缩工具用户指南](https://www.hiascend.com/document/detail/zh/canncommercial/850/devaids/amct/atlasamct_16_0001.html)[》中的“快速入门](https://www.hiascend.com/document/detail/zh/canncommercial/850/devaids/amct/atlasamct_16_0002.html)”获取量化原始模型和量化信息文件。
生成量化原始模型和量化信息文件说明如下：
- resnet50_quant.json：量化信息文件，记录了量化模型同原始模型节点的映射关系，用于量化后模型同原始模型精度比对使用。
- resnet50_deploy_model.prototxt：量化后的可在昇腾AI处理器部署的模型文件。
- resnet50_deploy_weights.caffemodel：量化后的可在昇腾AI处理器部署的权重文件。
- resnet50_fake_quant_model.prototxt：量化后的可在Caffe环境进行精度仿真模型文件。
- resnet50_fake_quant_weights.caffemodel：量化后的可在Caffe环境进行精度仿真权重文件。

resnet50_deploy_model.prototxt和resnet50_deploy_weights.caffemodel文件可用于进行ATC模型转换，resnet50_fake_quant_model.prototxt和resnet50_fake_quant_weights.caffemodel可用于进行Caffe量化原始模型的dump操作。

#### 量化离线模型文件

对量化原始模型文件resnet50_deploy_model.prototxt和resnet50_deploy_weights.caffemodel执行ATC模型转换，即可获取到量化离线模型文件和量化离线模型文件转换的json文件。

其中，量化原始模型文件从量化原始模型和量化信息文件操作中获取，ATC模型转换可参照全网层信息文件中的操作。
**父主题：**[GPU/CPU vs NPU（Caffe离线推理）](atlasaccuracy_16_0025.html)