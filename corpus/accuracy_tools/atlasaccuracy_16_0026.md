---
title: "总体说明"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/ModelAccuracyAnalyzer/atlasaccuracy_16_0026.html"
date_collected: "2026-05-04"
category: "accuracy_tools"
original_path: "zh/mindstudio/830/T&ITools/ModelAccuracyAnalyzer/atlasaccuracy_16_0026.html"
---

# 总体说明

[对于该场景需要排查比对结果说明](atlasaccuracy_16_0036.html#ZH-CN_TOPIC_0000002504183998)。

Caffe场景支持量化、非量化的精度比对。

- **非量化场景下**，需准备下表中的比对数据文件：**表1**非量化原始模型 vs 非量化离线模型的比对数据文件要求
文件

说明

获取方式

非量化原始模型的npy文件

标杆数据

[Caffe模型npy文件准备](atlasaccuracy_16_0027.html#ZH-CN_TOPIC_0000002536143807)

通过ATC转换离线模型文件生成的json文件

获取算子的映射关系

[全网层信息文件](atlasaccuracy_16_0030.html#ZH-CN_TOPIC_0000002504183994__zh-cn_topic_0000002502723508_section1145933865214)

非量化离线模型在昇腾AI处理器上运行生成的dump数据文件

待比对数据

离线推理场景各框架获取NPU环境的dump数据方法一致，请参考：

[准备离线模型dump数据文件](atlasaccuracy_16_0028.html#ZH-CN_TOPIC_0000002504343834)
|  |  |  |
| --- | --- | --- |
|  |  |  |
|  |  |  |
|  |  |  |

- **量化场景下**，若需要详细分析量化过程和模型转换阶段的精度问题，可按如下步骤比对：
  - **量化**[是指对模型的权重（weight）和数据（activation）进行低比特处理，让最终生成的网络模型更加轻量化，从而达到节省网络模型存储空间、降低传输时延、提高计算效率，达到性能提升与优化的目标。详情请参见《AMCT模型压缩工具用户指南](https://www.hiascend.com/document/detail/zh/canncommercial/850/devaids/amct/atlasamct_16_0001.html)》。
  - **AMCT对原始框架模型进行量化时，会插入量化和反量化算子，而使用ATC工具进行模型转换过程中，会对插入的量化和反量化算子进行融合，此情况下进行量化后模型dump结果与原始模型dump结果的比对可能不准确。因此如果用户想使用通过AMCT量化后的模型进行精度比对，则需要通过--fusion_switch_file**[参数关闭部分算子融合功能，并在精度比对后进行NPU vs NPU（离线推理）](atlasaccuracy_16_0032.html#ZH-CN_TOPIC_0000002536023775)，判断融合前后是否存在精度差异。

Caffe的离线推理场景，为了提升性能进行了模型量化，但模型量化后可能存在精度下降的问题。为了提升性能，一定的精度下降是可以接受的，一般一个模型精度下降在1%范围内，但如果误差较大，那么就需要定位原因。引起精度误差较大的原因主要有：

  - 量化过程导致精度下降。
  - 量化原始模型，经过ATC转换成的量化离线模型在NPU上运行，算子的变化导致精度问题。
根据以上原因，那么要分步骤定位精度问题：
  1. 定位量化阶段的精度问题。
执行非量化原始模型（GPU/CPU） vs 量化原始模型（GPU/CPU）。

    1. [参见Caffe模型npy文件准备](atlasaccuracy_16_0027.html#ZH-CN_TOPIC_0000002536143807)获取非量化原始模型resnet50.prototxt和resnet50.caffemodel的dump数据文件。
    2. [参见量化原始模型和量化信息文件](atlasaccuracy_16_0030.html#ZH-CN_TOPIC_0000002504183994__zh-cn_topic_0000002502723508_section124541012123819)，获取量化原始模型文件resnet50_deploy_model.prototxt和resnet50_deploy_weights.caffemodel、resnet50_fake_quant_model.prototxt和resnet50_fake_quant_weights.caffemodel以及量化信息文件resnet50_quant.json。
    3. [参见Caffe模型npy文件准备](atlasaccuracy_16_0027.html#ZH-CN_TOPIC_0000002536143807)获取量化原始模型resnet50_fake_quant_model.prototxt和resnet50_fake_quant_weights.caffemodel的dump数据文件。
    4. [参见比对操作和分析](atlasaccuracy_16_0031.html#ZH-CN_TOPIC_0000002504343832)执行非量化原始模型与量化原始模型的精度比对操作。
    5. 完成精度比对后首先确认量化模型精度误差多少。一般通过模型的批量数据的TopN的精度确认，例如1万~10万张图片的精度误差情况，如果在1%，基本上合理，无须定位，如果超过1%甚至达到3%，那么量化导致的精度问题不可忽略。
    6. 检测量化流程设计是否合理。例如选取的量化数据集是否具有代表性，是业务需要的数据集，数据量是否过少，一般10~100之间为正常。
    7. 若量化阶段精度误差较大，建议对模型首、尾2层进行手动去量化，一般可提升一部分精度。

  2. 定位模型转换阶段产生的精度问题，即量化离线模型在NPU上运行时的精度问题。
执行量化原始模型（GPU/CPU） vs 量化离线模型（关闭算子融合功能）（NPU）。

由于ATC工具的模型转换操作默认开启了算子融合功能，故为了排除融合后算子无法直接进行精度比对的因素，模型转换先关闭算子融合功能。

    1. 通过关闭算子融合功能执行ATC模型转换获取量化离线模型（关闭算子融合功能）。************
```
atc --model=$HOME/module/resnet50_deploy_model.prototxt --weight=$HOME/module/resnet50_deploy_weights.caffemodel --framework=0 --output=$HOME/module/out/caffe_resnet50_off --soc_version=<soc_version>  --fusion_switch_file=$HOME/module/fusion_switch.cfg
```

关闭算子融合功能需要通过--fusion_switch_file参数指定算子融合规则配置文件（如fusion_switch.cfg），并在配置文件中关闭算子融合功能。融合规则配置文件关闭配置如下：

```
 1
 2
 3
 4
 5
 6
 7
 8
 9
10
```

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
|  |  |
| --- | --- |

[详细参数解释请参见《ATC离线模型编译工具用户指南](https://www.hiascend.com/document/detail/zh/canncommercial/850/devaids/atctool/atlasatc_16_0031.html)》
若提示如下信息，则说明模型转换成功。
```
1
```

```
ATC run success

```
|  |  |
| --- | --- |

成功执行命令后，在$HOME/module/out/caffe_resnet50_off目录下生成离线模型（如：caffe_resnet50.om）。

    2. 生成json文件。******
```
atc --mode=1 --om=$HOME/module/out/caffe_resnet50_off/caffe_resnet50.om --json=$HOME/data/resnet50.json
```

    3. [参见准备离线模型dump数据文件](atlasaccuracy_16_0028.html#ZH-CN_TOPIC_0000002504343834)获取量化离线模型caffe_resnet50.om（关闭算子融合功能）的dump数据文件。
    4. [参见比对操作和分析](atlasaccuracy_16_0031.html#ZH-CN_TOPIC_0000002504343832)执行量化原始模型与量化离线模型（关闭算子融合功能）的精度比对操作。
    5. [若模型转换阶段精度误差较大，根据比对结果判断是累计误差，还是某个节点误差较大，如果是某一阶段误差较大，您可以获取日志后单击Link](https://www.hiascend.com/support)联系技术支持。规避方法：建议对该节点手动去量化，重新进行模型量化。如果是累计误差，可以检查是否为量化阶段的误差，由于量化本身存在精度损失，所以如果是量化产生的精度误差，那么可能有大量算子均存在较小的精度误差，可以通过调整量化配置重复量化，直至满足精度要求。
    6. [特殊数据：由于余弦相似度不能完全衡量精度，所以在如上方法还不能解决的情况，可以进行单算子比对](atlasaccuracy_16_0047.html#ZH-CN_TOPIC_0000002536143817)。

  3. [（可选）参见NPU vs NPU（离线推理）](atlasaccuracy_16_0032.html#ZH-CN_TOPIC_0000002536023775)的“开启和关闭算子融合功能模型转换的精度比对”场景执行量化离线模型（默认开启算子融合功能）与量化离线模型（关闭算子融合功能）的精度比对操作。

- **量化场景下**，若只需要初步判断非量化原始模型（GPU/CPU）到量化离线模型（NPU）的精度问题，按照下表准备比对数据文件：**表2**非量化原始模型 vs 量化离线模型的比对数据文件要求
文件

说明

获取方式

非量化原始模型的npy文件

标杆数据

[Caffe模型npy文件准备](atlasaccuracy_16_0027.html#ZH-CN_TOPIC_0000002536143807)

  - 通过ATC转换离线模型文件生成的json文件
  - AMCT后的量化信息文件（*.json）

二选一

获取算子的映射关系

[准备模型文件和量化信息文件](atlasaccuracy_16_0030.html#ZH-CN_TOPIC_0000002504183994)

量化离线模型在昇腾AI处理器上运行生成的dump数据文件

待比对数据

[准备离线模型dump数据文件](atlasaccuracy_16_0028.html#ZH-CN_TOPIC_0000002504343834)
|  |  |  |
| --- | --- | --- |
|  |  |  |
|  |  |  |
|  |  |  |

**父主题：**[GPU/CPU vs NPU（Caffe离线推理）](atlasaccuracy_16_0025.html)