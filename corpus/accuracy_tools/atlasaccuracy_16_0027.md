---
title: "Caffe模型npy文件准备"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/ModelAccuracyAnalyzer/atlasaccuracy_16_0027.html"
date_collected: "2026-05-04"
category: "accuracy_tools"
original_path: "zh/mindstudio/830/T&ITools/ModelAccuracyAnalyzer/atlasaccuracy_16_0027.html"
---

# Caffe模型npy文件准备

#### 前提条件

- [针对量化原始模型获取npy文件，请先参见量化原始模型和量化信息文件](atlasaccuracy_16_0030.html#ZH-CN_TOPIC_0000002504183994__zh-cn_topic_0000002502723508_section124541012123819)获取量化原始模型。
- [为确保生成符合命名要求的.npy文件，需要对原始的Caffe模型文件去除in-place，生成新的.prototxt模型文件用于生成.npy文件（例如：如果有未去除in-place的A、B、C、D四个融合算子，进行dump数据，输出的结果为D算子的结果，但命名却是A算子开头，就会导致比对时找不到文件）。针对量化场景，需要先在环境上安装AMCT再执行去除in-place命令，AMCT安装方法请参见《AMCT模型压缩工具用户指南](https://www.hiascend.com/document/detail/zh/canncommercial/850/devaids/amct/atlasamct_16_0001.html)[》中的“安装工具](https://www.hiascend.com/document/detail/zh/canncommercial/850/devaids/amct/atlasamct_16_0030.html)”。
进入/home/xxx/Ascend/cann/tools/operator_cmp/compare目录，执行命令去除in-place，命令行举例如下：
**
```
python3 inplace_layer_process.py -i /home/user/resnet50.prototxt
```

执行命令后，在/home/user目录下生成去除in-place的new_resnet50.prototxt文件。

- 针对量化场景：为确保精度误差，需要保证执行Caffe模型推理时的预处理数据与Caffe AMCT时的预处理数据一致。

#### 生成npy文件

本版本不提供Caffe模型numpy数据生成功能，请自行安装Caffe环境并提前准备Caffe原始数据“*.npy”文件。本文仅提供生成符合精度比对要求的numpy格式Caffe原始数据“*.npy”文件的样例参考。

[如何准备原始Caffe模型npy文件，您可以参见论坛发帖算子精度比对工具标杆数据生成环境搭建指导（Caffe + TensorFlow）](https://bbs.huaweicloud.com/blogs/181059)或者自行获取其他方法。该帖仅供参考。

为输出符合精度比对要求的“*.npy”文件，需在推理结束后的代码中增加dump操作，示例代码如下：

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
11
12
13
14
15
16
17
18
```

```
    # 读取prototxt文件
    net_param = caffe_pb2.NetParameter()
    with open(self.model_file_path, 'rb') as model_file:
        google.protobuf.text_format.Parse(model_file.read(), net_param)

        # 保存数据为numpy文件
        for layer in net_param.layer:
            name = layer.name.replace("/", "_").replace(".", "_")
            index = 0
            for top in layer.top:
                data = net.blobs[top].data[...]
                file_name = name + "." + str(index) + "." + str(
                    round(time.time() * 1000000)) + ".npy"
                output_dump_path = os.path.join(self.output_path, file_name)
                np.save(output_dump_path, data)
                print('The dump data of "' + layer.name
                      + '" has been saved to "' + output_dump_path + '".')
                index += 1

```
|  |  |
| --- | --- |

增加上述代码后，运行Caffe模型的应用工程，即可生成符合要求的npy文件。

- 需要根据代码中的output_dump_path参数在当前目录新建对应“onnx_dump”目录或自定义目录。
- *npy文件命名格式为{op_name}.{output_index}.{timestamp}**.npy，其中需要确保文件名中的{output_index}*字段存在值为0，否则无比对结果，原因是精度比对时默认从第一个output_index为0的数据开始。
**父主题：**[GPU/CPU vs NPU（Caffe离线推理）](atlasaccuracy_16_0025.html)