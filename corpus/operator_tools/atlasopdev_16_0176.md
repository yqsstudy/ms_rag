---
title: "检测Triton算子"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0176.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0176.html"
---

# 检测Triton算子

#### 前提条件

- [参考Link](https://gitcode.com/Ascend/triton-ascend)，完成Triton及Triton-Ascend插件的安装和配置。
- 为了防止未重新编译的算子造成影响，建议您启用以下环境变量：
```
export TRITON_ALWAYS_COMPILE=1
```

- 自备Triton算子实现文件。若用户尚未准备Triton算子，可参考以下示例。本节将基于此示例来说明Triton算子的检测流程。
```
# file name: sample.py
import triton
import triton.language as tl
import torch

def torch_pointwise(x0, x1):
    res = x0 + x1
    return res

@triton.jit
def triton_add(in_ptr0, in_ptr1, out_ptr0, XBLOCK: tl.constexpr, XBLOCK_SUB: tl.constexpr):
    offset = tl.program_id(0) * XBLOCK
    base1 = tl.arange(0, XBLOCK_SUB)
    loops1: tl.constexpr = (XBLOCK + XBLOCK_SUB - 1) // XBLOCK_SUB
    for loop1 in range(loops1):
        x0 = offset + (loop1 * XBLOCK_SUB) + base1
        tmp0 = tl.load(in_ptr0 + (x0), None)
        tmp1 = tl.load(in_ptr1 + (x0), None)
        tmp2 = tmp0 + tmp1
        tl.store(out_ptr0 + (x0), tmp2, None)

def test_case(dtype, shape, ncore, xblock, xblock_sub):
    x0 = torch.randn(shape, dtype=dtype).npu()
    x1 = torch.randn(shape, dtype=dtype).npu()
    y_ref = torch_pointwise(x0, x1)
    y_cal = torch.zeros(shape, dtype=dtype).npu()
    triton_add[ncore, 1, 1](x0, x1, y_cal, xblock, xblock_sub)
    print("Pass" if torch.equal(y_ref, y_cal) else "Failed")

if __name__ == "__main__":
    test_case(torch.float32, (2, 4096, 8), 2, 32768, 1024)
```

#### 操作步骤

1. [请参考Triton算子调用场景](atlasopdev_16_0040.html#ZH-CN_TOPIC_0000002536800523__zh-cn_topic_0000002534506457_li338910473313)准备，完成使用前准备。
2. 关闭内存池。
样例中使用PyTorch创建Tensor，PyTorch框架内默认使用内存池的方式管理GM内存，会对内存检测产生干扰。因此，在检测前需要额外设置如下环境变量关闭内存池，以保证检测结果准确。
```
export PYTORCH_NO_NPU_MEMORY_CACHING=1
```

3. 在Triton算子中构造一个非法读写的场景，将第一次load的内存向右偏移100个元素，此时会导致load在GM内存上发生非法读。
****
```
def triton_add(in_ptr0, in_ptr1, out_ptr0, XBLOCK: tl.constexpr, XBLOCK_SUB: tl.constexpr):
    offset = tl.program_id(0) * XBLOCK
    base1 = tl.arange(0, XBLOCK_SUB)
    loops1: tl.constexpr = (XBLOCK + XBLOCK_SUB - 1) // XBLOCK_SUB
    for loop1 in range(loops1):
        x0 = offset + (loop1 * XBLOCK_SUB) + base1
        # ERROR: 构造非法读异常
        tmp0 = tl.load(in_ptr0 + (x0) + 100, None)
        tmp1 = tl.load(in_ptr1 + (x0), None)
```

4. [使用msSanitizer检测工具拉起Triton算子。具体参数说明请参考表2](atlasopdev_16_0039.html#ZH-CN_TOPIC_0000002505040558__zh-cn_topic_0000002534426413_zh-cn_topic_0000001691887174_table716213104506)[和表3](atlasopdev_16_0039.html#ZH-CN_TOPIC_0000002505040558__zh-cn_topic_0000002534426413_zh-cn_topic_0000001691887174_table1796112119339)[，内存检测请参考内存检测](atlasopdev_16_0042.html#ZH-CN_TOPIC_0000002536920491)。

```
mssanitizer -t memcheck -- python sample.py
```

#### 内存异常报告示例
根据检测工具输出的报告，可以发现在sample.py的18行对GM存在368字节的非法读操作，与构造的异常场景一致。
```
1
2
3
4
5
6
7
8
```

```
$ mssanitizer -t memcheck -- python sample.py
[mssanitizer] logging to file: ./mindstudio_sanitizer_log/mssanitizer_20250522093805_922880.log
Failed
====== ERROR: illegal read of size 368
======    at 0x12c0c0053190 on GM in triton_add
======    in block aiv(1) on device 0
======    code in pc current 0x1b0 (serialNo:524)
======    #0 sample.py:18:45

```
|  |  |
| --- | --- |
**父主题：**[典型案例](atlasopdev_16_0044.html)