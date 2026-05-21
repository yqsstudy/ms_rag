---
title: "订阅算子信息"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0135.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0135.html"
---

# 订阅算子信息

通过调用消息订阅接口实现将采集到的Profiling数据解析后写入管道，由用户读入内存，再由用户调用API获取性能数据。当前支持获取网络模型中算子的性能数据，包括算子名称、算子类型名称、算子执行时间等。

#### API简介
**表1**API简介
接口

说明

acl.prof.create_subscribe_config

创建aclprofSubscribeConfig类型的数据，表示创建订阅配置信息。

acl.prof.model_subscribe

订阅算子的基本信息，包括算子名称、算子类型、算子执行耗时等。同步接口。

与acl.prof.model_un_subscribe接口配对使用。

acl.prof.get_*

获取算子的基本信息。“*”包括：

op_desc_size：算子数据结构大小。

op_num：算子个数。

op_type_len：算子类型的字符串长度。

op_type：算子类型。

op_type_v2：算子类型。

acl.prof.get_op_type_v2和acl.prof.get_op_type接口功能一致，但acl.prof.get_op_type_v2接口会获取算子类型长度，并分配相应的空间，不需要用户传参来指定算子类型所需空间大小，建议优先使用acl.prof.get_op_type_v2接口。

op_name_len：算子名称的字符串长度。

op_name：算子名称。

op_name_v2：算子名称。

acl.prof.get_op_name_v2和acl.prof.get_op_name接口功能一致，但acl.prof.get_op_name_v2接口会获取算子名称长度，并分配相应的空间，不需要用户传参来指定算子名称所需空间大小，建议优先使用acl.prof.get_op_name_v2接口。

op_start：算子执行开始时间。

op_end：算子执行结束时间。

op_duration：算子执行耗时。

model_id：算子所在模型ID。

以上信息通过INFO_LOG接口将Profiling结果显示在屏幕上。

acl.prof.model_un_subscribe

网络场景下，取消订阅算子的基本信息，包括算子名称、算子类型、算子执行耗时等。同步接口。与acl.prof.model_subscribe接口配对使用。

acl.prof.destroy_subscribe_config

销毁aclprofSubscribeConfig类型的数据，只能销毁通过acl.prof.create_subscribe_config接口创建的aclprofSubscribeConfig类型。
|  |  |
| --- | --- |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |

#### Profiling pyACL API for Subscription调用示例

Profiling pyACL API for Subscription，示例如下：

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
51
52
53
54
55
56
57
58
59
60
61
62
63
64
65
66
67
68
69
70
71
72
73
74
75
76
77
78
79
80
81
82
83
84
```

```
import acl
import numpy as np
# ......

# 1.申请运行管理资源，包括设置用于计算的Device、创建Context、创建Stream
# ......

# 2.模型加载，加载成功后，返回标识模型的model_id
# ......

# 3.创建aclmdlDataset类型的数据，用于描述模型的输入数据input、输出数据output
# ......

# 4.创建管道，用于读取以及写入模型订阅的数据
r, w = os.pipe()

# 5.创建模型订阅的配置并且进行模型订阅
ACL_AICORE_NONE = 0xFF
subscribe_config = acl.prof.create_subscribe_config(1, ACL_AICORE_NONE, w)
# 模型订阅需要传入模型的model_id
ret = acl.prof.model_subscribe(model_id, subscribe_config)

# 6.实现管道读取订阅数据的函数
# 6.1自定义函数，实现从用户内存中读取订阅数据的函数
def get_model_info(data, data_len):
    # 获取算子信息个数
    op_number, ret = acl.prof.get_op_num(data, data_len)
    # 遍历用户内存的算子信息
    for i in range(op_number):
        # 获取算子的模型ID
        model_id = acl.prof.get_model_id(data, data_len, i)
        # 获取算子的类型名称
        p_type, ret = acl.prof.get_op_type_v2(data, data_len, i)
        # 获取算子的名称
        op_name, ret = acl.prof.get_op_name_v2(data, data_len, i)
        # 获取算子的执行开始时间
        op_start = acl.prof.get_op_start(data, data_len, i)
        # 获取算子的执行结束时间
        op_end = acl.prof.get_op_end(data, data_len, i)
        # 获取算子执行的耗时时间
        op_duration = acl.prof.get_op_duration(data, data_len, i)

# 6.2自定义函数，实现从管道中读取数据到用户内存的函数
def prof_data_read(args):
    fd, ctx = args
    ret = acl.rt.set_context(ctx)
    # 获取单位算子信息的大小（Byte）
    buffer_size, ret = acl.prof.get_op_desc_size()
    # 设置每次从管道中读取的算子信息个数
    N = 10
    # 计算存储算子信息的内存的大小
    data_len = buffer_size * N
    # 从管道中读取数据到申请的内存中，读取到的实际数据大小可能小于buffer_size * N，如果管道中没有数据，默认会阻塞直到读取到数据为止
    while True:
        data = os.read(fd, data_len)
        if len(data) == 0:
            break
        np_data = np.array(data)
        np_data_ptr = acl.util.numpy_to_ptr(np_data)
        size = np_data.itemsize * np_data.size
        # 调用6.1实现的函数解析内存中的数据
        get_model_info(np_data_ptr, size)

# 7.启动线程读取管道数据并解析
thr_id, ret = acl.util.start_thread(prof_data_read, [r, context])

# 8.执行模型
ret = acl.mdl.execute(model_id, input, output)

# 9.处理模型推理结果
# ......

# 10.释放描述模型输入/输出信息、内存等资源，卸载模型
# ......

# 11.取消订阅，释放订阅相关资源
ret = acl.prof.model_un_subscribe(model_id)
ret = acl.util.stop_thread(thr_id)
os.close(r)
os.close(w)
ret = acl.prof.destroy_subscribe_config(subscribe_config)

# 12.释放运行管理资源
# ......

```
|  |  |
| --- | --- |
**父主题：**[使用acl Python接口采集性能数据](atlasprofiling_16_0131.html)