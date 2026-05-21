---
title: "PyTorch多卡大集群场景如何避免性能数据直接落盘到共享存储时导致的性能膨胀问题"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0315.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0315.html"
---

# PyTorch多卡大集群场景如何避免性能数据直接落盘到共享存储时导致的性能膨胀问题

#### 故障现象

PyTorch多卡大集群场景在使用Ascend PyTorch Profiler接口采集并落盘性能数据时，通过使用on_trace_ready执行tensorboard_trace_handler函数的方式进行性能数据落盘。

采集性能数据的耗时膨胀。

#### 故障原因

由于使用on_trace_ready执行tensorboard_trace_handler函数，将落盘路径直接指向了共享存储，多卡数据大量的落盘请求导致共享存储响应延迟。

#### 故障处理

通过自定义on_trace_ready的落盘方式，将性能数据先落盘到本地，再将本地的性能数据拷贝到共享存储，可解决性能膨胀问题，示例代码如下：

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
```

```
import time
import torch
import torch_npu
import os
import random
import string
import shutil
import argparse
from torch_npu.profiler._profiler_path_creator import ProfPathCreator
def generate_random_filename(length=8):
    letters = string.ascii_lowercase
    random_letters = ''.join(random.choice(letters) for _ in range(length))
    return random_letters
def create_random_directory():
    random_filename = generate_random_filename()
    file_path = os.path.join("/tmp/", f"{random_filename}")
    return file_path
def move_file_to_user_path(file_path, user_input_path):
    try:
        if not os.path.exists(user_input_path):
            os.makedirs(user_input_path)
        for item in os.listdir(file_path):
            source_item = os.path.join(file_path, item)
            destination_item = os.path.join(user_input_path, item)
            shutil.move(source_item, destination_item)
        os.rmdir(file_path)
        return True
    except Exception as e:
        print(str(e))
        return False
def train_one_step(i):
    print(f"[APP]train: {i} step...")
    a = torch.rand(2, 3).to("npu")
    b = torch.rand(2, 3).to("npu")
    c = a + b
    time.sleep(2)

# 如下user_tensorboard_trace_handler为on_trace_ready的自定义函数，ori_path为本地路径，dst_path为共享存储路径
def user_tensorboard_trace_handler(ori_path, dst_path, dir_name: str = None, worker_name: str = None, analyse_flag: bool = True):
    ProfPathCreator().init(worker_name=worker_name, dir_name=dir_name)
    def handler_fn(prof_inst) -> None:
        if analyse_flag:
            prof_inst.prof_if.analyse()
        result = move_file_to_user_path(ori_path, dst_path)
        if result is True:
            print(f"文件已成功移动到路径：{dst_path}")
        else:
            print(f"移动文件时出错：{result}")
    return handler_fn

def main():
    parser = argparse.ArgumentParser(description="Generate a random txt file and move it to the specified path.")
    parser.add_argument("path", help="Target path where the file will be moved")
    args = parser.parse_args()
    random_txt_file_path = create_random_directory()
    # 如下on_trace_ready调用了user_tensorboard_trace_handler自定义函数
    prof = torch_npu.profiler.profile(on_trace_ready=user_tensorboard_trace_handler(random_txt_file_path, args.path, random_txt_file_path),
    schedule=torch_npu.profiler.schedule(skip_first=1, repeat=1, active=2, wait=0, warmup=0))
    prof.start()
    step_num = 5
    for i in range(step_num):
        train_one_step(i)
        prof.step()
    prof.stop()
if __name__ == "__main__":
    main()

```
|  |  |
| --- | --- |
**父主题：**[FAQ](atlasprofiling_16_0314.html)