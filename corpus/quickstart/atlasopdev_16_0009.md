---
title: "创建算子工程（msOpGen）"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/msquickstart/atlasopdev_16_0009.html"
date_collected: "2026-05-04"
category: "quickstart"
original_path: "zh/mindstudio/830/msquickstart/atlasopdev_16_0009.html"
---

# 创建算子工程（msOpGen）

msOpGen工具用于算子开发时，可生成自定义算子工程，方便用户专注于算子的核心逻辑和算法实现，而无需花费大量时间在项目搭建、编译配置等重复性工作上，从而提高了开发效率。

1. 生成算子目录。

  1. [把算子定义的AddCustom.json文件放到工作目录当中，json文件的配置参数详细说明请参考《算子开发工具用户指南](https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0002.html)[》的“算子工程创建（msOpGen）> 创建算子工程](https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0021.html)”章节。
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
[
    {
        "op": "AddCustom",
        "language": "cpp",
        "input_desc": [
            {
                "name": "x",
                "param_type": "required",
                "format": [
                    "ND"
                ],
                "type": [
                    "float16"
                ]
            },
            {
                "name": "y",
                "param_type": "required",
                "format": [
                    "ND"
                ],
                "type": [
                    "float16"
                ]
            }
        ],
        "output_desc": [
            {
                "name": "z",
                "param_type": "required",
                "format": [
                    "ND"
                ],
                "type": [
                    "float16"
                ]
            }
        ]
    }
]

```
|  |  |
| --- | --- |

  2. [执行以下命令，生成算子开发工程，参数说明请参见《算子开发工具用户指南](https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0002.html)[》的“算子工程创建（msOpGen）> 工具概述](https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0018.html)”章节。****
```
msopgen gen -i AddCustom.json -f tf -c ai_core-ascendxxxyy -lan cpp -out AddCustom  # xxxyy为用户实际使用的具体芯片类型
```

  3. 执行以下命令，查看生成目录。
```
tree -C -L 2 AddCustom/
```

  4. 在指定目录下生成的算子工程目录。
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
```

```
AddCustom
├── build.sh               // 编译入口脚本
├── cmake
├── CMakeLists.txt         // 算子工程的CMakeLists.txt
├── CMakePresets.json      // 编译配置项
├── framework             // 算子插件实现文件目录，单算子模型文件的生成不依赖算子适配插件，无需关注
│   ├── CMakeLists.txt
│   └── tf_plugin
├── op_host                // Host侧实现文件
│   ├── add_custom.cpp       // 算子原型注册、shape推导、信息库、tiling实现等内容文件
│   ├── add_custom_tiling.h  // 算子tiling定义文件
│   └── CMakeLists.txt
├── op_kernel                 // Kernel侧实现文件
│   ├── add_custom.cpp      // 算子代码实现文件 
│   └── CMakeLists.txt
└── scripts                 // 自定义算子工程打包相关脚本所在目录

```
|  |  |
| --- | --- |

2. [单击Link](https://gitee.com/ascend/samples/tree/master/operator/ascendc/0_introduction/1_add_frameworklaunch/AddCustom)，获取算子核函数开发和Tiling实现的代码样例。执行以下命令，将样例目录中的算子实现文件移动至msOpGen步骤1生成的目录中。

```
cp -r ${git_clone_path}/samples/operator/ascendc/0_introduction/1_add_frameworklaunch/AddCustom/* AddCustom/
```

  - ${git_clone_path}为sample仓的存放路径。
  - [完成算子工程创建后，需参考《Ascend C算子开发指南](https://www.hiascend.com/document/detail/zh/canncommercial/850/opdevg/Ascendcopdevg/atlas_ascendc_map_10_0002.html)》进行算子开发，但此步骤只需体现算子开发工具的功能，因此直接使用代码样例。
  - 下载代码样例时，需执行以下命令指定分支版本。
```
git clone https://gitee.com/ascend/samples.git -b r0.2
```

3. 编译算子工程。

  1. [参考《算子开发工具用户指南](https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0002.html)[》的“算子工程创建（msOpGen）> 算子编译部署 > 编译前准备](https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0024.html)”章节，完成编译相关配置。
  2. 在算子工程目录下，执行如下命令，进行算子工程编译。编译完成后，将会在build_out目录生成.run算子包。****
```
./build.sh
```

4. 在自定义算子包所在路径下，执行如下命令，部署算子包。
******************
```
./build_out/custom_opp_<target_os>_<target_architecture>.run
```

5. **验证算子功能，生成可执行文件execute_add_op**。

  1. 切换到AclNNInvocation仓的目录。
```
cd ${git_clone_path}/samples/operator/ascendc/0_introduction/1_add_frameworklaunch/AclNNInvocation
```

  2. 执行以下命令。
```
./run.sh
```

  3. 成功对比精度，并生成可执行文件execute_add_op
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
```

```
INFO: execute op!
[INFO]  Set device[0] success
[INFO]  Get RunMode[1] success
[INFO]  Init resource success
[INFO]  Set input success
[INFO]  Copy input[0] success
[INFO]  Copy input[1] success
[INFO]  Create stream success
[INFO]  Execute aclnnAddCustomGetWorkspaceSize success, workspace size 0
[INFO]  Execute aclnnAddCustom success
[INFO]  Synchronize stream success
[INFO]  Copy output[0] success
[INFO]  Write output success
[INFO]  Run op success
[INFO]  Reset Device success
[INFO]  Destroy resource success
INFO: acl executable run success!
error ratio: 0.0000, tolerance: 0.0010
test pass

```
|  |  |
| --- | --- |

**父主题：**[算子开发工具快速入门](tools_qucikstart_0006.html)