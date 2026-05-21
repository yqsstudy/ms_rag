---
title: "准备Caffe模型npy文件"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/ModelAccuracyAnalyzer/atlasaccuracy_16_0069.html"
date_collected: "2026-05-04"
category: "accuracy_tools"
original_path: "zh/mindstudio/830/T&ITools/ModelAccuracyAnalyzer/atlasaccuracy_16_0069.html"
---

# 准备Caffe模型npy文件

本版本不提供Caffe模型npy文件生成功能，请自行安装Caffe环境并提前准备Caffe原始数据“*.npy”文件。本文仅提供生成符合精度比对要求的numpy格式Caffe原始数据“*.npy”文件的样例参考。

[如何准备原始Caffe模型npy文件，您可以参考论坛发帖算子精度比对工具标杆数据生成环境搭建指导（Caffe + TensorFlow）](https://bbs.huaweicloud.com/blogs/181059)或者自行获取其他方法。该帖仅供参考。

[如果您需要使用二进制格式dump文件进行比对，请参见如何进行npy文件转dump文件](atlasaccuracy_16_0076.html#ZH-CN_TOPIC_0000002504184018)完成npy文件转换成dump文件。

Caffe原始npy文件准备要求：

- 文件内容以numpy格式保存。
- *文件命名以{op_name}.{output_index}.{timestamp}*.npy形式命名。设置numpy数据文件名包括output_index字段且值为0，确保转换生成的dump数据的output_index为0。因为精度比对时，默认从第一个output_index为0的数据开始，否则无比对结果。
- [为确保生成符合命名要求的.npy文件，需要对原始的Caffe模型文件去除in-place，生成新的.prototxt模型文件用于生成.npy文件（例如：如果有未去除in-place的A、B、C、D四个融合算子，进行dump数据，输出的结果为D算子的结果，但命名却是A算子开头，就会导致比对时找不到文件）。针对量化场景，需要先在环境上安装AMCT再执行去除in-place命令，安装方法请参见《AMCT模型压缩工具用户指南](https://www.hiascend.com/document/detail/zh/canncommercial/850/devaids/amct/atlasamct_16_0001.html)》。
${INSTALL_DIR}/tools/operator_cmp/compare，${INSTALL_DIR}请替换为CANN软件安装后文件存储路径。以root用户安装为例，则安装后文件存储路径为：/usr/local/Ascend/cann。

执行命令去除in-place，命令行举例如下：
**
```
python3 inplace_layer_process.py -i /home/user/resnet50.prototxt
```

执行命令后，在/home/user目录下生成去除in-place的new_resnet50.prototxt文件。

- 针对量化场景：为确保精度误差在合理范围内，需要执行Caffe模型推理时预处理数据与Caffe昇腾模型压缩时预处理数据一致。

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
    # read prototxt file
    net_param = caffe_pb2.NetParameter()        
    with open(self.model_file_path, 'rb') as model_file:
        google.protobuf.text_format.Parse(model_file.read(), net_param)

        # save data to numpy file
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

增加上述代码后，运行Caffe模型的应用工程，即可生成符合要求的“*.npy”文件。
**父主题：**[比对数据准备](atlasaccuracy_16_0066.html)