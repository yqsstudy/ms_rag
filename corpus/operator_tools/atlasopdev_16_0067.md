---
title: "内存与变量打印"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0067.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0067.html"
---

# 内存与变量打印

根据变量类型和用法，变量可以存储在寄存器中或存储在Local Memory、Global Memory内存中，用户可以打印变量的地址以找出它的存储位置并进一步打印关联的内存。

#### 打印变量

命中断点后，使用 p variable_name 的命令形式可打印指定的变量的值，比如：

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
(msdebug) p alpha
(float) $0 = 0.00100000005
(msdebug) p tiling
(const TCubeTiling) $1 = {
  usedCoreNum = 2
  M = 1024
  N = 640
  Ka = 256
  ...
}

```
|  |  |
| --- | --- |

目前msDebug工具不支持直接通过变量名打印模板参数的值，需要通过p 模板参数对应的对象的方式进行打印，在打印后的类型里展示模板参数的值。例如COMPUTE_LENGTH为模板参数，this为该模板参数所属的对象指针，若要打印该参数的值，可以在使用该参数的位置，通过命令p this进行打印，示例如下：

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
```

```
   22   template<class ArchTag_, class ElementAccumulator_, class ElementOut_, uint32_t COMPUTE_LENGTH>
   23   struct ReduceAdd {
   24       ReduceAdd(Arch::Resource<ArchTag> &resource)
   25       {
 -> 26            for (uint32_t i = 0; i < BUFFER_NUM; i++) {
   27               inputBuffer[i] = resource.ubBuf.template GetBufferByByte<ElementAccumulator>(bufferOffset);
   28               bufferOffset += COMPUTE_LENGTH * sizeof(ElementAccumulator);
(msdebug) p this
(Catlass::Gemm::Kernel::ReduceAdd<Catlass::Arch::AtlasA2, float, __fp16, 32> *) $0 = 0x00000000001cf838

```
|  |  |
| --- | --- |

#### 打印GlobalTensor

GlobalTensor一般用来存放Global Memory（外部存储）的全局数据。

**输入以下命令，进行GlobalTensor变量打印。以cGlobal为例，zGm所在内存地址请参考address_**字段，此处为“0x000012c045400000”。

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
(msdebug) p cGlobal
(AscendC::GlobalTensor<float>) $0 = {
  AscendC::BaseGlobalTensor<float> = {
    address_ = 0x000012c045400000
    oriAddress_ = 0x000012c045400000
  }
  bufferSize_ = 655360
  shapeInfo_ = {
    shapeDim = '\0'
    originalShapeDim = '\0'
    shape = ([0] = 0, [1] = 0, [2] = 0, [3] = 0, [4] = 0, [5] = 0, [6] = 0, [7] = 0)
    originalShape = ([0] = 0, [1] = 0, [2] = 0, [3] = 0, [4] = 0, [5] = 0, [6] = 0, [7] = 0)
    dataFormat = ND
  }
  cacheMode_ = CACHE_MODE_NORMAL
}

```
|  |  |
| --- | --- |

因GlobalTensor类型变量实际的值保存在GM内存中，输入以下命令，打印GM内存中位于地址“0x000012c045400000”上的值，打印格式设置为：打印1行，每行256字节，按照float32格式打印。

```
1
2
```

```
(msdebug) x -m GM -f float32[] 0x000012c045400000 -s 256 -c 1
0x12c045400000: {4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096}

```
|  |  |
| --- | --- |

- 若需要打印其他自定义地址，用户需自行保证该自定义地址的合法性，否则可能会导致算子运行出错。
- 若需要以自定义地址为起始进行内存打印，可基于address_字段作为起始地址增加偏移，偏移量单位为字节数，得到偏移后的GM内存地址后，传入内存打印命令即可。

#### 打印LocalTensor

LocalTensor一般用于存放AI Core中Local Memory（内部存储）的数据。

输入以下命令，进行LocalTensor变量打印，以reluOutLocal为例，reluOutLocal所在内存地址请参考address_字段中的bufferAddr参数，此处位于0上，长度为131072。

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
```

```
(msdebug) p reluOutLocal
(AscendC::LocalTensor<float>) $2 = {
  AscendC::BaseLocalTensor<float> = {
    address_ = (dataLen = 131072, bufferAddr = 0, bufferHandle = "", logicPos = '\n')
  }
  shapeInfo_ = {
    shapeDim = '\0'
    originalShapeDim = '\0'
    shape = ([0] = 0, [1] = 1092616192, [2] = 4800, [3] = 1473680, [4] = 0, [5] = 1473888, [6] = 0, [7] = 1471968)
    originalShape = ([0] = 0, [1] = 3222199212, [2] = 4800, [3] = 1, [4] = 0, [5] = 1473376, [6] = 0, [7] = 1473376)
    dataFormat = ND
  }
}

```
|  |  |
| --- | --- |

该Tensor变量的实际内容保存在UB内存中，输入以下命令，打印UB内存中位于地址0上的值，打印格式设置为：打印1行，每行256字节，按照float32格式打印。

- **本用例中，Tensor变量的实际内容保存在UB上，但LocalTensor不一定都保存在UB中，也可能在L1/L0A/L0B上，需要用户根据代码自行判断，然后在打印命令的-m**选项中选择正确的内存类型。
- 若需要以自定义地址为起始进行内存打印，可基于address_字段作为起始地址增加偏移，偏移量单位为字节数，得到偏移后的GM内存地址后，传入内存打印命令即可。

```
1
2
```

```
(msdebug) x -m UB -f float32[] 0 -s 256 -c 1
0x00000000: {4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096 4096}

```
|  |  |
| --- | --- |

#### 打印所有局部变量
输入以下命令，打印当前作用域所有局部变量。
```
1
2
3
4
5
6
7
```

```
(msdebug) var
(MatmulLeakyKernel<__fp16, __fp16, float, float> *__stack__) this = 0x0000000000167b60
(uint32_t) count = 0
(const uint32_t) roundM = 2
(const uint32_t) roundN = 5
(uint32_t) startOffset = 0
(AscendC::DataCopyParams) copyParam = (blockCount = 256, blockLen = 16, srcStride = 0, dstStride = 64)

```
|  |  |
| --- | --- |

**父主题：**[算子调试（msDebug）](atlasopdev_16_0061.html)