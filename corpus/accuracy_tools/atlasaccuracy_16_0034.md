---
title: "准备离线模型文件"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/ModelAccuracyAnalyzer/atlasaccuracy_16_0034.html"
date_collected: "2026-05-04"
category: "accuracy_tools"
original_path: "zh/mindstudio/830/T&ITools/ModelAccuracyAnalyzer/atlasaccuracy_16_0034.html"
---

# 准备离线模型文件

#### 非量化离线模型文件

[以下介绍通过ATC模型转换工具获取离线模型的操作步骤，更多操作请参见《ATC离线模型编译工具用户指南](https://www.hiascend.com/document/detail/zh/canncommercial/850/devaids/atctool/atlasatc_16_0031.html)》。

1. 以运行用户登录Ascend-cann-toolkit所在环境。
2. 获取原始模型文件并保存在任意目录下。

例如：resnet50.prototxt和resnet50.caffemodel

3. 开启算子融合功能执行ATC模型转换。
**********
```
atc --model=$HOME/module/resnet50.prototxt --weight=$HOME/module/resnet50.caffemodel --framework=0 --output=$HOME/module/out/caffe_resnet50_on --soc_version=<soc_version> 
```

模型转换时，算子融合功能默认开启，无需配置。
若提示如下信息，则说明模型转换成功。
```
1
```

```
ATC run success

```
|  |  |
| --- | --- |

成功执行命令后，在$HOME/module/out/目录下生成离线模型（如：caffe_resnet50_on.om）。

4. 关闭算子融合功能执行ATC模型转换。
************
```
atc --model=$HOME/module/resnet50.prototxt --weight=$HOME/module/resnet50.caffemodel --framework=0 --output=$HOME/module/out/caffe_resnet50_off --soc_version=<soc_version>  --fusion_switch_file=$HOME/module/fusion_switch.cfg
```

关闭算子融合功能需要通过--fusion_switch_file参数指定算子融合规则配置文件（如fusion_switch.cfg），并在配置文件中关闭算子融合功能。融合规则配置文件关闭配置如下：

```
{
    "Switch":{
        "GraphFusion":{
            "ALL":"off"
        },
        "UBFusion":{
            "ALL":"off"
         }
    }
}
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

成功执行命令后，在$HOME/module/out/目录下生成离线模型（如：caffe_resnet50_off.om）。

#### 量化离线模型文件

[以下仅以Caffe模型为例介绍通过AMCT模型压缩工具获取量化信息文件的操作步骤，更多操作请参见《AMCT模型压缩工具用户指南](https://www.hiascend.com/document/detail/zh/canncommercial/850/devaids/amct/atlasamct_16_0001.html)》。

1. [参见《AMCT模型压缩工具用户指南](https://www.hiascend.com/document/detail/zh/canncommercial/850/devaids/amct/atlasamct_16_0001.html)[》的“安装工具](https://www.hiascend.com/document/detail/zh/canncommercial/850/devaids/amct/atlasamct_16_0030.html)”章节完成工具安装。
2. 获取原始模型文件并保存在任意目录下。

例如：resnet50.prototxt和resnet50.caffemodel

3. 准备模型相匹配的二进制数据集。

  1. 切换到amct_caffe/cmd目录，执行如下命令，用于下载校准数据集。
```
cd data 
mkdir image && cd image
wget https://obs-9be7.obs.cn-east-2.myhuaweicloud.com/models/amct_acl/classification/calibration.rar
unrar e calibration.rar
```

  2. 在amct_caffe/cmd目录，执行如下命令将calibration目录下*.jpg格式数据集转换为bin格式数据集。
```
python3 ./src/process_data.py
```

执行完成后，在data目录会生成新的calibration目录，并在该目录生成calibration.bin格式数据集。

4. 执行如下命令进行网络模型的量化操作。
************
```
amct_caffe calibration --model=./model/resnet50.prototxt --weights=./model/resnet50.caffemodel --save_path=./results --input_shape="data:1,3,224,224" --data_dir="./data/calibration" --data_types="float32"
```

5. 若提示如下信息且无Error日志信息，则说明模型量化成功。

```
1
2
```

```
INFO - [AMCT]:[Utils]: The weights_file is saved in $HOME/xxx/results/resnet50_fake_quant_weights.caffemodel
INFO - [AMCT]:[Utils]: The model_file is saved in $HOME/xxx/results/resnet50_fake_quant_model.prototxt

```
|  |  |
| --- | --- |
量化后生成文件说明如下：
  - resnet50_quant.json：量化信息文件，记录了量化模型同原始模型节点的映射关系，用于量化后模型同原始模型精度比对使用。
  - resnet50_deploy_model.prototxt：量化后的可在昇腾AI处理器部署的模型文件。
  - resnet50_deploy_weights.caffemodel：量化后的可在昇腾AI处理器部署的权重文件。
  - resnet50_fake_quant_model.prototxt：量化后的可在Caffe环境进行精度仿真模型文件。
  - resnet50_fake_quant_weights.caffemodel：量化后的可在Caffe环境进行精度仿真权重文件。

6. 按照非量化离线模型文件中的ATC操作将量化原始模型文件resnet50_deploy_model.prototxt和resnet50_deploy_weights.caffemodel进行模型转换，即可获取到开启和关闭算子融合功能的量化离线模型文件。
**父主题：**[NPU vs NPU（离线推理）](atlasaccuracy_16_0032.html)