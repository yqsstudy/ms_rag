---
title: "检测内核调用符方式的Ascend C算子"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0045.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0045.html"
---

# 检测内核调用符方式的Ascend C算子

#### 操作步骤

1. [请参考内核调用符场景准备](atlasopdev_16_0040.html#ZH-CN_TOPIC_0000002536800523__zh-cn_topic_0000002534506457_li159191517103114)，完成使用前准备。
2. [参考使用前准备](atlasopdev_16_0040.html#ZH-CN_TOPIC_0000002536800523)完成相关环境变量的配置。
3. 构建单算子可执行文件。

以Add算子为例，可执行文件的构建命令示例如下：
******
```
bash run.sh -r npu -v <soc_version> 
```

*一键式编译运行脚本完成后，在工程目录下生成NPU侧可执行文件<kernel_name>_npu*。

4. *使用msSanitizer检测工具拉起单算子可执行文件（以add_npu*为例）。

  - [内存检测执行以下命令，具体参数说明请参考表2](atlasopdev_16_0039.html#ZH-CN_TOPIC_0000002505040558__zh-cn_topic_0000002534426413_zh-cn_topic_0000001691887174_table716213104506)[和表3](atlasopdev_16_0039.html#ZH-CN_TOPIC_0000002505040558__zh-cn_topic_0000002534426413_zh-cn_topic_0000001691887174_table1796112119339)，内存检测请参考内存检测示例说明。**
```
mssanitizer --tool=memcheck ./add_npu   # 内存检测需指定 --tool=memcheck
```

  - [竞争检测执行以下命令，具体参数说明请参考表2](atlasopdev_16_0039.html#ZH-CN_TOPIC_0000002505040558__zh-cn_topic_0000002534426413_zh-cn_topic_0000001691887174_table716213104506)，竞争检测请参考竞争检测示例说明。**
```
mssanitizer --tool=racecheck ./add_npu  # 竞争检测需指定 --tool=racecheck
```

单算子可执行文件所在路径可配置为绝对路径或相对路径，请根据实际环境配置。

#### 内存检测示例说明

- 在步骤1之前，需要在Add算子中构造一个非法读写的场景，将DataCopy内存拷贝长度从TILE_LENGTH改为2 * TILE_LENGTH，此时最后一次拷贝会发生内存读写越界。
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
  __aicore__ inline void CopyOut(int32_t progress)
    {
        // deque output tensor from VECOUT queue
        LocalTensor<half> zLocal = outQueueZ.DeQue<half>();
        // copy progress_th tile from local tensor to global tensor
        // 构造非法读写场景
        DataCopy(zGm[progress * TILE_LENGTH], zLocal, 2 * TILE_LENGTH);
        // free output tensor for reuse
        outQueueZ.FreeTensor(zLocal);
    }

```
|  |  |
| --- | --- |

- **根据检测工具输出的报告，可以发现在add_custom.cpp**的65行对GM存在224字节的非法写操作，与我们构造的异常场景对应。
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
```

```
$ mssanitizer --tool=memcheck ./add_npu
====== ERROR: illegal write of size 224
======    at 0x12c0c002ef00 on GM in add_custom_kernel
======    in block aiv(7) on device 0
======    code in pc current 0x1644 (serialNo:2342)
======    #0 ${ASCEND_HOME_PATH}/compiler/tikcpp/tikcfw/impl/dav_c220/kernel_operator_data_copy_impl.h:107:9
======    #1 ${ASCEND_HOME_PATH}/compiler/tikcpp/tikcfw/inner_interface/inner_kernel_operator_data_copy_intf.cppm:155:9
======    #2 ${ASCEND_HOME_PATH}/compiler/tikcpp/tikcfw/inner_interface/inner_kernel_operator_data_copy_intf.cppm:459:5
======    #3 samples/operator/AddCustomSample/KernelLaunch/AddKernelInvocation/add_custom.cpp:65:9
======    #4 samples/operator/AddCustomSample/KernelLaunch/AddKernelInvocation/add_custom.cpp:38:13
======    #5 samples/operator/AddCustomSample/KernelLaunch/AddKernelInvocation/add_custom.cpp:82:8

```
|  |  |
| --- | --- |

#### 竞争检测示例说明

- 在步骤1之前，需要在Add算子中构造一个核间竞争的场景，将DataCopy内存拷贝长度从TILE_LENGTH改为2 * TILE_LENGTH，此时会在GM内存上存在核间竞争。
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
  __aicore__ inline void CopyOut(int32_t progress)
    {
        // deque output tensor from VECOUT queue
        LocalTensor<half> zLocal = outQueueZ.DeQue<half>();
        // copy progress_th tile from local tensor to global tensor
        // 构造核间竞争场景
        DataCopy(zGm[progress * TILE_LENGTH], zLocal, 2 * TILE_LENGTH);
        // free output tensor for reuse
        outQueueZ.FreeTensor(zLocal);
    }

```
|  |  |
| --- | --- |

- **根据检测工具输出的报告，可以发现在add_kernel.cpp**的65行，AIV的0核和1核存在核间竞争，符合我们构造的异常场景。
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
$ mssanitizer --tool=racecheck ./add_npu
====== ERROR: Potential WAW hazard detected at GM in add_custom_kernel:
======    PIPE_MTE3 Write at WAW()+0x12c0c0025f00 in block 0 (aiv) on device 0 at pc current 0x1644 (serialNo:305)
======    #0 ${ASCEND_HOME_PATH}/compiler/tikcpp/tikcfw/impl/dav_c220/kernel_operator_data_copy_impl.h:107:9
======    #1 ${ASCEND_HOME_PATH}/compiler/tikcpp/tikcfw/inner_interface/inner_kernel_operator_data_copy_intf.cppm:155:9
======    #2 ${ASCEND_HOME_PATH}/compiler/tikcpp/tikcfw/inner_interface/inner_kernel_operator_data_copy_intf.cppm:459:5
======    #3 samples/operator/AddCustomSample/KernelLaunch/AddKernelInvocation/add_custom.cpp:65:9
======    #4 samples/operator/AddCustomSample/KernelLaunch/AddKernelInvocation/add_custom.cpp:38:13
======    #5 samples/operator/AddCustomSample/KernelLaunch/AddKernelInvocation/add_custom.cpp:82:8
======    PIPE_MTE3 Write at WAW()+0x12c0c0026000 in block 1 (aiv) on device 0 at pc current 0x1644 (serialNo:329)
======    #0 ${ASCEND_HOME_PATH}/compiler/tikcpp/tikcfw/impl/dav_c220/kernel_operator_data_copy_impl.h:107:9
======    #1 ${ASCEND_HOME_PATH}/compiler/tikcpp/tikcfw/inner_interface/inner_kernel_operator_data_copy_intf.cppm:155:9
======    #2 ${ASCEND_HOME_PATH}/compiler/tikcpp/tikcfw/inner_interface/inner_kernel_operator_data_copy_intf.cppm:459:5
======    #3 samples/operator/AddCustomSample/KernelLaunch/AddKernelInvocation/add_custom.cpp:65:9
======    #4 samples/operator/AddCustomSample/KernelLaunch/AddKernelInvocation/add_custom.cpp:38:13
======    #5 samples/operator/AddCustomSample/KernelLaunch/AddKernelInvocation/add_custom.cpp:82:8

```
|  |  |
| --- | --- |

**父主题：**[典型案例](atlasopdev_16_0044.html)