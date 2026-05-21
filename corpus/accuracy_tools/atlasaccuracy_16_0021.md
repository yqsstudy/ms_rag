---
title: "准备ONNX模型npy文件"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/ModelAccuracyAnalyzer/atlasaccuracy_16_0021.html"
date_collected: "2026-05-04"
category: "accuracy_tools"
original_path: "zh/mindstudio/830/T&ITools/ModelAccuracyAnalyzer/atlasaccuracy_16_0021.html"
---

# 准备ONNX模型npy文件

#### 前提条件

- 需要确保每个算子节点有名称，否则无法生成正确的文件名。没有名称的算子节点需要先生成名称。
- 本参考示例以每个节点只有一个输出为例，多个输出的需要在文件名生成处适配output_index的获取。

#### 代码参考示例

本版本不提供ONNX模型npy文件生成功能，请自行安装ONNX环境并提前准备ONNX原始数据npy文件。本文提供的样例代码仅作参考。

为输出符合精度比对要求的npy文件，需在推理结束后的代码中增加dump操作，示例代码如下：

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
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
```

```
import os
import onnx
import onnxruntime
import numpy as np
import time

from skl2onnx.helpers.onnx_helper import enumerate_model_node_outputs
from skl2onnx.helpers.onnx_helper import select_model_inputs_outputs
from skl2onnx.helpers.onnx_helper import save_onnx_model

# 修改模型，增加输出节点
model_onnx = onnx.load("./resnet50.onnx")
output = []
for out in enumerate_model_node_outputs(model_onnx):
    output.append(out)

num_onnx = select_model_inputs_outputs(model_onnx,outputs=output)
save_onnx_model(num_onnx, "resnet50_dump.onnx")

# 推理得到输出，本示例中采用随机数作为输入
input_data = np.random.random((1,3,224,224)).astype(np.float32)
input_data.tofile("test_data.bin")
sess = onnxruntime.InferenceSession("resnet50_dump.onnx")
input_name = sess.get_inputs()[0].name
output_name = [node.name for node in sess.get_outputs()]
res = sess.run(output_name, {input_name: input_data})

# 获得输出名称，确保每个算子节点有对应名称
node_name = [node.name for node in model_onnx.graph.node]

# 保存数据
node_output_num = [len(node.output) for node in model_onnx.graph.node]
idx = 0
for num, name in zip(node_output_num, node_name):
    for i in range(num):
        data = res[idx] 
        file_name = name + "." + str(i) + "." + str(round(time.time() * 1000000)) + ".npy"
        output_dump_path = os.path.join("./onnx_dump/", file_name)
        np.save(output_dump_path, data.astype(np.float16))
        idx += 1

```
|  |  |
| --- | --- |

- 需要根据代码中的output_dump_path参数在当前目录新建对应“onnx_dump”目录或自定义目录。
- *npy文件命名格式为{op_name}.{output_index}.{timestamp}**.npy，其中需要确保文件名中的{output_index}*字段存在值为0，否则无比对结果，原因是精度比对时默认从第一个output_index为0的数据开始。
**父主题：**[GPU vs NPU（ONNX离线推理）](atlasaccuracy_16_0019.html)