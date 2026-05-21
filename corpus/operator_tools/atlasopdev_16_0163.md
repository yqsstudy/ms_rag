---
title: "autotune"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0163.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0163.html"
---

# autotune

#### 功能说明

遍历搜索空间，尝试不同参数组合，展示每个组合的运行耗时与最优组合。

#### 函数原型

```
def autotune(configs: List[Dict], warmup: int = 300, repeat: int = 1, device_ids = [0]):
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

warmup

输入

采集性能前的设备预热时间。通常情况下，预热时间越长，采集到的算子性能越稳定。

单位：微秒。

可选参数，默认值：1000，取值范围为1~100000之间的整数。

repeat

输入

重放次数，会根据多次重放取运行耗时的平均值作为算子耗时。

可选参数，默认值：1，取值范围为1~10000之间的整数。

device_ids

输入

Device ID列表，目前仅支持单Device模式，如果填写多个Device ID，只有第一个会生效。

可选参数，默认值：[0]。
|  |  |  |
| --- | --- | --- |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |

#### 返回值说明

无。

#### 调用示例

```
@mskpp.autotune(configs=[
    {'L1TileShape': 'MatmulShape<64, 64, 64>', 'L0TileShape': 'MatmulShape<128, 256, 64>'},
    {'L1TileShape': 'MatmulShape<64, 64, 128>', 'L0TileShape': 'MatmulShape<128, 256, 64>'},
    {'L1TileShape': 'MatmulShape<64, 128, 128>', 'L0TileShape': 'MatmulShape<128, 256, 64>'},
    {'L1TileShape': 'MatmulShape<64, 128, 128>', 'L0TileShape': 'MatmulShape<64, 256, 64>'},
    {'L1TileShape': 'MatmulShape<128, 128, 128>', 'L0TileShape': 'MatmulShape<128, 256, 64>'},
], warmup=500, repeat=10, device_ids=[0])
def basic_matmul(problem_shape, a, layout_a, b, layout_b, c, layout_c):
    kernel = get_kernel()
    blockdim = 20
    return kernel[blockdim](problem_shape, a, layout_a, b, layout_b, c, layout_c)
```
**父主题：**[接口列表](atlasopdev_16_0156.html)