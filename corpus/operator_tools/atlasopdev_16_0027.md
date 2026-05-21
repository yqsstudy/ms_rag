---
title: "Ascend C自定义算子开发实践"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0027.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0027.html"
---

# Ascend C自定义算子开发实践

展示如何使用msOpGen工具进行Ascend C自定义算子的工程创建、编译和部署，并使用msOpST工具对Ascend C自定义算子进行功能测试。

#### 前提条件

[已参考使用前准备](atlasopdev_16_0019.html#ZH-CN_TOPIC_0000002504880712)，完成msOpGen工具的使用准备。

#### 操作步骤

1. 参考以下json文件，准备算子原型文件（以MatmulCustom算子为例）。

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
41
42
43
44
45
46
47
48
49
50
```

```
[
    {
        "op": "MatmulCustom",
        "language": "cpp",
        "input_desc": [
            {
                "name": "a",
                "param_type": "required",
                "format": [
                    "ND"
                ],
                "type": [
                    "float16"
                ]
            },
            {
                "name": "b",
                "param_type": "required",
                "format": [
                    "ND"
                ],
                "type": [
                    "float16"
                ]
            },
            {
                "name": "bias",
                "param_type": "required",
                "format": [
                    "ND"
                ],
                "type": [
                    "float"
                ]
            }
        ],
        "output_desc": [
            {
                "name": "c",
                "param_type": "required",
                "format": [
                    "ND"
                ],
                "type": [
                    "float"
                ]
            }
        ]
    }
]

```
|  |  |
| --- | --- |

2. 使用msOpGen工具执行以下命令，创建算子工程。

[msOpGen工具仅生成空的算子工程模板，需要用户自行添加算子实现，具体请参考《Ascend C算子开发指南](https://www.hiascend.com/document/detail/zh/canncommercial/850/opdevg/Ascendcopdevg/atlas_ascendc_map_10_0002.html)[》中的工程化算子开发](https://www.hiascend.com/document/detail/zh/canncommercial/850/opdevg/Ascendcopdevg/atlas_ascendc_10_0059.html)章节。
**
```
msopgen gen -i MatmulCustom.json -f tf -c ai_core-Ascendxxxyy -lan cpp -out MatmulCustom
```

3. 命令执行完毕，会在指定目录下生成如下算子工程目录。

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
```

```
MatmulCustom/
├── build.sh         // 编译入口脚本
├── cmake 
│   ├── xx.cmake
│   ├── ....
│   ├── util        // 算子工程编译所需脚本及公共编译文件存放目录
├── CMakeLists.txt   // 算子工程的CMakeLists.txt
├── CMakePresets.json // 编译配置项
├── framework        // 算子插件实现文件目录，单算子模型文件的生成不依赖算子适配插件，无需关注
├── op_host                      // Host侧实现文件
│   ├── matmul_custom_tiling.h    // 算子tiling定义文件
│   ├── matmul_custom.cpp         // 算子原型注册、shape推导、信息库、tiling实现等内容文件
│   ├── CMakeLists.txt
├── op_kernel                   // Kernel侧实现文件
│   ├── CMakeLists.txt   
│   ├── matmul_custom.cpp        // 算子代码实现文件 
├── scripts                     // 自定义算子工程打包相关脚本所在目录

```
|  |  |
| --- | --- |

4. 执行算子工程编译。

```
./build.sh
```

5. 进行自定义算子包部署。

  - 执行以下命令，将算子部署到CANN：********
```
./build_out/custom_opp_<target_os>_<target_architecture>.run
```

  - *执行以下命令，将算子部署到自定义路径（以xxx*/MatmulCustom/installed为例）：**************
```
./build_out/custom_opp_<target_os>_<target_architecture>.run --install-path="xxx/MatmulCustom/installed" 
```

6. 执行以下命令，生成ST测试用例。
************
```
msopst create -i "xxx/MatmulCustom/op_host/matmul_custom.cpp" -out ./st  // xxx需要修改为用户实际工程路径
```

7. 进行ST测试。

  1. 根据CANN包安装路径，配置以下环境变量：**
```
export DDK_PATH=${INSTALL_DIR}
export NPU_HOST_LIB=${INSTALL_DIR}/{arch-os}/devlib
```

  2. 执行以下命令，进行ST测试，并将输出结果到指定路径：******************
```
msopst run -i ./st/xxx.json -soc Ascendxxxyy -out ./st/out  //xxx.json为步骤6获得的测试用例
```

**父主题：**[典型案例](atlasopdev_16_0026.html)