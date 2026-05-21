---
title: "分级可视化构图比对"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/msquickstart/atlasquick_train_0012.html"
date_collected: "2026-05-04"
category: "quickstart"
original_path: "zh/mindstudio/830/msquickstart/atlasquick_train_0012.html"
---

# 分级可视化构图比对

#### 前提条件

- [完成环境准备](atlasquick_train_0002.html#ZH-CN_TOPIC_0000002502572164__section68892049173411)。
- 安装tb-graph-ascend。
```
pip install tb-graph-ascend
```

- [完成精度数据采集](atlasquick_train_0008.html)。

#### 执行比对

1. 创建比对配置文件。以在训练脚本所在目录创建compare.json配置文件为例，文件内容拷贝如下示例配置。
```
1
2
3
4
5
```

```
{
"npu_path": "./dump_data_2.7.0",
"bench_path": "./dump_data_2.6.0",
"is_print_compare_log": true
}

```
|  |  |
| --- | --- |

其中"npu_path"和"bench_path"对应的路径需要在同一环境下。

2. 执行图构建比对。****
```
msprobe -f mindspore graph -i ./compare.json -o ./output
```

比对完成后在./output下生成vis后缀文件。

3. 启动TensorBoard。**
```
tensorboard --logdir ./output --bind_all
```

--logdir指定的路径即为2中的./output路径。

执行以上命令后打印如下日志。

```
1
```

```
TensorBoard 2.19.0 at http://ubuntu:6008/ (Press CTRL+C to quit)

```
|  |  |
| --- | --- |

需要在Windows环境下打开浏览器，访问地址http://ubuntu:6008/，其中ubuntu修改为服务器的IP地址，例如http://192.168.1.10:6008/。

访问地址成功后页面显示TensorBoard界面，如下所示。
**图1**
分级可视化构图比对
由于本样例在dump数据时"level"配置为"L1"，故采集到模型结构数据为空，分级可视化构图时无数据，如上图为其他数据示例。

**父主题：**[精度比对](atlasquick_train_0010.html)