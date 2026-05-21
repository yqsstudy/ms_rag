---
title: "mstxRangeStartA"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/API/mstxAPIReference/atlasopdev_16_0117.html"
date_collected: "2026-05-04"
category: "mstx_api"
original_path: "zh/mindstudio/830/API/mstxAPIReference/atlasopdev_16_0117.html"
---

# mstxRangeStartA

#### 产品支持情况

产品

是否支持

Atlas A3 训练系列产品/Atlas A3 推理系列产品

√

Atlas A2 训练系列产品/Atlas A2 推理系列产品

√

Atlas 200I/500 A2 推理产品

√

Atlas 推理系列产品

√

Atlas 训练系列产品

√
|  |  |
| --- | --- |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |

#### 功能说明

mstx range指定范围能力的起始位置标记。

#### 函数原型

C/C++：

```
mstxRangeId mstxRangeStartA(const char *message, aclrtStream stream)
```

Python：

```
mstx.range_start(message, stream)
```

#### 参数说明
**表1**参数说明
参数

输入/输出

说明

message

输入

message为标记的文字，携带打点信息。

C/C++中数据类型：const char *。

Python中，message为字符串。

默认None。

传入的message字符串长度要求：

- MSPTI场景：不能超过255字节。
- 非MSPTI场景（例如msprof命令行、Ascend PyTorch Profiler）：不能超过156字节。
说明：
message不能传入空指针。

stream

输入

stream表示使用mark的线程。

C/C++中数据类型：aclrtStream。

Python中stream是aclrtStream对象。

默认None。

- 配置为nullptr时，只标记Host侧的瞬时事件。
- 配置为有效的stream时，标识Host侧和对应Device侧的瞬时事件。
|  |  |  |
| --- | --- | --- |
|  |  |  |
|  |  |  |

#### 返回值

如果返回0，则表示失败。

#### 调用示例

- C/C++调用方法：************
```
...
bool RunOp()
{
// create op desc
...
const char *message = "h1";
mstxRangeId id = mstxRangeStartA(message, NULL);
...
// Run op
if
(!opRunner.RunOp()) {
ERROR_LOG("Run
op failed");
return false;
}
mstxRangeEnd(id);
...
}
```

- **Python**调用方法一：
通过Python API接口，以C/C++语言实现相关接口内容并编译生成so，相关so在PYTHONPATH中可以被Python直接引用。

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
import mstx
mstx.range_start("aaa")
print(1)
mstx.range_end(1)
import torch
import torch_npu
a = torch.Tensor([1,2,3,4]).npu()
b = torch.Tensor([1,2,3,4]).npu()
hi_str = "hi"
hello_str = "hello"
hi_id = mstx.range_start(hi_str, None)
c = a + b
hello_id = mstx.range_start(hello_str, stream=None)
d = a - b
mstx.range_end(hi_id)
e = a * b
mstx.range_end(hello_id)

```
|  |  |
| --- | --- |

- **Python**调用方法二：
直接使用Python开发，通过ctypes.CDLL("libms_tools_ext.so")直接引用原mstx的so文件，并使用其中提供的API。

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
```

```
import mstx
import torch
import torch_npu
import acl
import sys
import ctypes
lib = ctypes.CDLL("libms_tools_ext.so")
# 定义函数的参数类型和返回类型
lib.mstxRangeStartA.argtypes = [ctypes.c_char_p, ctypes.c_void_p]
lib.mstxRangeStartA.restype = ctypes.c_uint64
lib.mstxRangeEnd.argtypes = [ctypes.c_uint64]
lib.mstxRangeEnd.restype = None
a = torch.Tensor([1,2,3,4]).npu()
b = torch.Tensor([1,2,3,4]).npu()
# 创建一个ctypes.c_char_p指针
hi_str = b"hi"
hi_ptr = ctypes.c_char_p(hi_str)
hi_id = ctypes.c_uint64()
# 创建一个ctypes.c_char_p指针
hello_str = b"hello"
hello_ptr = ctypes.c_char_p(hello_str)
hello_id = ctypes.c_uint64()
# 调用函数
hi_id.value = lib.mstxRangeStartA(hi_ptr, None)
c = a + b
hello_id.value = lib.mstxRangeStartA(hello_ptr, None)
d = a - b
lib.mstxRangeEnd(hi_id)
e = a * b
lib.mstxRangeEnd(hello_id)

```
|  |  |
| --- | --- |