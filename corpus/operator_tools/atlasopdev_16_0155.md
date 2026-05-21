---
title: "快速入门"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0155.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0155.html"
---

# 快速入门

本章节以单算子00_basic_matmul为例，帮助用户快速上手msKPP工具的Kernel级自动调优功能。

#### 操作步骤

1. [执行以下命令，下载Link](https://gitcode.com/cann/catlass/tree/catlass-v1-stable)中的Ascend C模板库。

```
git clone https://gitcode.com/cann/catlass.git -b catlass-v1-stable
```

2. 进入模板库中的00_basic_matmul样例代码目录。

```
cd catlass/examples/00_basic_matmul
```

3. 修改basic_matmul.cpp文件，在L1TileShape、L0TileShape变量声明的行末尾添加注释 （// tunable）。

```
// basic_matmul.cpp
...
51 using L1TileShape = GemmShape<128, 256, 256>; // tunable
52 using L0TileShape = GemmShape<128, 256, 64>; // tunable
...
```

4. [将附录中Python脚本文件basic_matmul_autotune.py](atlasopdev_16_0157.html#ZH-CN_TOPIC_0000002504880704)[与编译脚本文件jit_build.sh](atlasopdev_16_0164.html#ZH-CN_TOPIC_0000002505040524)保存至00_basic_matmul目录中。
5. 运行样例脚本basic_matmul_autotune.py。

```
$ python3 basic_matmul_autotune.py 
No.0: 22.562μs, {'L1TileShape': 'GemmShape<128, 256, 256>', 'L0TileShape': 'GemmShape<128, 256, 64>'}
No.1: 22.109μs, {'L1TileShape': 'GemmShape<128, 256, 128>', 'L0TileShape': 'GemmShape<128, 256, 64>'}
No.2: 17.778μs, {'L1TileShape': 'GemmShape<128, 128, 256>', 'L0TileShape': 'GemmShape<128, 128, 64>'}
No.3: 15.378μs, {'L1TileShape': 'GemmShape<64, 128, 128>', 'L0TileShape': 'GemmShape<64, 128, 128>'}
No.4: 14.982μs, {'L1TileShape': 'GemmShape<64, 128, 256>', 'L0TileShape': 'GemmShape<64, 128, 128>'}
No.5: 15.671μs, {'L1TileShape': 'GemmShape<64, 128, 512>', 'L0TileShape': 'GemmShape<64, 128, 128>'}
No.6: 19.592μs, {'L1TileShape': 'GemmShape<64, 64, 128>', 'L0TileShape': 'GemmShape<64, 64, 128>'}
No.7: 18.340μs, {'L1TileShape': 'GemmShape<64, 64, 256>', 'L0TileShape': 'GemmShape<64, 64, 128>'}
No.8: 18.541μs, {'L1TileShape': 'GemmShape<64, 64, 512>', 'L0TileShape': 'GemmShape<64, 64, 128>'}
No.9: 20.652μs, {'L1TileShape': 'GemmShape<128, 128, 128>', 'L0TileShape': 'GemmShape<128, 128, 128>'}
No.10: 17.728μs, {'L1TileShape': 'GemmShape<128, 128, 256>', 'L0TileShape': 'GemmShape<128, 128, 128>'}
No.11: 17.637μs, {'L1TileShape': 'GemmShape<128, 128, 512>', 'L0TileShape': 'GemmShape<128, 128, 128>'}
Best config: No.4
compare success.
```

以上打印数据表示在算子代码basic_matmul.cpp中，L1TileShape定义为GemmShape<64, 128, 256>且L0TileShape定义为GemmShape<64, 128, 128>时，性能最优。

**父主题：**[自动调优](atlasopdev_16_0153.html)