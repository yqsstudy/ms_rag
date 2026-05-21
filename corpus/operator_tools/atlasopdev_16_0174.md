---
title: "调用示例"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0174.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0174.html"
---

# 调用示例

[本章节以matmulleakyrelu算子工程为例，介绍如何利用msKPP工具提供的mskpp.tiling_func](atlasopdev_16_0185.html#ZH-CN_TOPIC_0000002536920433)[和mskpp.get_kernel_from_binary](atlasopdev_16_0186.html#ZH-CN_TOPIC_0000002504880688)接口调用msOpGen工程中的tiling函数以及用户自定义的Kernel函数，其他类型的算子操作均可参考此流程进行操作。

#### 环境准备

- [请参考环境准备](atlasopdev_16_0003.html#ZH-CN_TOPIC_0000002536800441)，完成相关环境变量的配置。
- [单击Link](https://gitee.com/ascend/samples/tree/master/operator/ascendc/0_introduction/12_matmulleakyrelu_frameworklaunch)获取样例工程，为进行算子检测做准备。
  - ${git_clone_path}为sample仓的存放路径。
  - 本样例工程以Atlas A2 训练系列产品/Atlas A2 推理系列产品为例。
  - 下载代码样例时，需执行以下命令指定分支版本。
```
git clone https://gitee.com/ascend/samples.git -b master
```

#### 具体操作

1. 参见环境准备中的样例工程，运行${git_clone_path}/operator/ascendc/0_introduction/12_matmulleakyrelu_frameworklaunch目录下的install.sh脚本，生成自定义算子工程，并进行Host侧和Kernel侧的算子实现。

```
bash install.sh -v Ascendxxxyy    # xxxyy为用户实际使用的具体芯片类型
```

2. 切换至自定义算子工程目录。

```
cd CustomOp
```

3. 编辑算子拉起脚本matmulleakyrelu.py。
[](atlasopdev_16_0025.html#ZH-CN_TOPIC_0000002505040542__zh-cn_topic_0000002502586584_zh-cn_topic_0000001823418621_zh-cn_topic_0000001650160328_table197301923143513)[](atlasopdev_16_0024.html#ZH-CN_TOPIC_0000002504880720__zh-cn_topic_0000002502586626_zh-cn_topic_0000001691887130_li1557111451225)
```
import numpy as np
import mskpp
# 这个函数的入参必须和Kernel函数的入参一致
def run_kernel(input_a, input_b, input_bias, output, workspace, tiling_data):
    kernel_binary_file = "MatmulLeakyreluCustom.o"    #不同的硬件和操作系统展示的.o文件的名称稍有不同，具体路径请参考表1中的-reloc参数
    kernel = mskpp.get_kernel_from_binary(kernel_binary_file, 'mix')
    return kernel(input_a, input_b, input_bias, output, workspace, tiling_data)

if __name__ == "__main__":
    # input/output tensor
    M = 1024
    N = 640
    K = 256
    input_a = np.random.randint(1, 10, [M, K]).astype(np.float16)
    input_b = np.random.randint(1, 10, [K, N]).astype(np.float16)
    input_bias = np.random.randint(1, 10, [N]).astype(np.float32)
    output = np.zeros([M, N]).astype(np.float32)
    # shape info
    inputs_info = [{"shape": [M, K], "dtype": "float16", "format": "ND"},
                   {"shape": [K, N], "dtype": "float16", "format": "ND"},
                   {"shape": [N], "dtype": "float32", "format": "ND"}]
    outputs_info = [{"shape": [M, N], "dtype": "float32", "format": "ND"}]
    attr = {}
    # 调用tiling函数
    tiling_output = mskpp.tiling_func(
        op_type="MatmulLeakyreluCustom",
        inputs_info=inputs_info, outputs_info=outputs_info, # 可选
        inputs=[input_a, input_b, input_bias], outputs=[output],
        attr=attr, # 可选
        lib_path="liboptiling.so",  # tiling代码编译产物，具体位置可参考算子编译部署中的步骤2中的目录结构
        # soc_version="", # 可选
    )
    blockdim = tiling_output.blockdim
    workspace_size = tiling_output.workspace_size
    tiling_data = tiling_output.tiling_data # numpy数组
    workspace = np.zeros(workspace_size).astype(np.uint8) # workspace需要用户自行申请
    # 调用Kernel函数
    run_kernel(input_a, input_b, input_bias, output, workspace, tiling_data)

    # 校验输出
    alpha = 0.001
    golden = (np.matmul(input_a.astype(np.float32), input_b.astype(np.float32)) + input_bias).astype(np.float32)
    golden = np.where(golden >= 0, golden, golden * alpha)
    is_equal = np.array_equal(output, golden)
    result = "success" if is_equal else "failed"
    print("compare {}.".format(result))
```

4. 运行脚本。

```
python3 matmulleakyrelu.py
```

**父主题：**[调用msOpGen算子工程](atlasopdev_16_0172.html)