---
title: "autotune_v2"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0171.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0171.html"
---

# autotune_v2

#### 功能说明

遍历搜索空间，尝试不同参数组合，展示每个组合的运行耗时与最优组合。

#### 函数原型

```
def autotune_v2(configs: List[Dict], warmup_times = 5)
```

#### 参数说明

参数名

输入/输出

说明

configs

输入

搜索空间定义。

数据类型：list[dict]。

必选参数。

warmup_times

输入

采集性能前的设备预热次数。

可选参数，默认值：5，取值范围为1~500之间的整数。
|  |  |  |
| --- | --- | --- |
|  |  |  |
|  |  |  |

#### 返回值说明

无。

#### 调用示例

```
@mskpp.autotune_v2(configs=[
    {'L1TileShape': 'GemmShape<128, 256, 256>', 'L0TileShape': 'GemmShape<128, 256, 64>'},
    {'L1TileShape': 'GemmShape<256, 128, 256>', 'L0TileShape': 'GemmShape<256, 128, 64>'},
    {'L1TileShape': 'GemmShape<128, 128, 256>', 'L0TileShape': 'GemmShape<128, 128, 64>'},
    {'L1TileShape': 'GemmShape<128, 128, 512>', 'L0TileShape': 'GemmShape<128, 128, 64>'},
    {'L1TileShape': 'GemmShape<64, 256, 128>', 'L0TileShape': 'GemmShape<64, 256, 64>'},
], warmup_times=10)
def run_executable(m, n, k, device_id):
    src_file = "./basic_matmul.cpp"
    build_script = "./jit_build_executable.sh" # executable compile script
    executable = mskpp.compile_executable(build_script=build_script, src_file=src_file, use_cache=False)
    return executable(m, n, k, device_id)
```
**父主题：**[接口列表](atlasopdev_16_0156.html)