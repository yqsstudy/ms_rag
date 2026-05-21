---
title: "改图优化"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_191.html"
date_collected: "2026-05-04"
category: "llm_cases"
original_path: "zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_191.html"
---

# 改图优化

如果自动优化无法满足目标，也已经识别到模型中存在一些冗余计算，或者需要通过调整数据类型使其从AI CPU运行切换到AI Core运行等场景时，可以通过改图的方式来进行性能优化。

以在GlobalAveragePool操作前加入Cast操作为例，改图脚本如下：

```
import onnx
from onnx import helper, TensorProto
from onnx import shape_inference
model_path = "D:\\035-Code\\om_test\\resnet50.onnx"
model = onnx.load(model_path)
def create_cast_node(input_name, output_name, to_type):
    return helper.make_node(
        'Cast',
        inputs=[input_name],
        outputs=[output_name],
        to=to_type
    )
for i, node in enumerate(model.graph.node):
    if node.op_type == 'GlobalAveragePool':
        # 获取GlobalAveragePool节点的输入
        input_name = node.input[0]
        # 生成新的Cast节点的输出名称
        cast_output_name = f"{input_name}_cast"
        # 创建Cast节点
        cast_node = create_cast_node(input_name, cast_output_name, TensorProto.FLOAT)
        # 更新GlobalAveragePool节点的输入
        node.input[0] = cast_output_name
        # 将Cast节点插入到计算图中
        model.graph.node.insert(i, cast_node)
        break  # 只处理第一个找到的GlobalAveragePool节点
output_model_path = "D:\\035-Code\\om_test\\resnet50_new.onnx"  # 替换为你想要保存的模型路径
onnx.save(model, output_model_path)
```

脚本执行后，效果如图1所示。
**图1**
**执行后效果

父主题：**[优化方法](toolsample6_094.html)