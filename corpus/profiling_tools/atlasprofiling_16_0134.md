---
title: "使用msproftx扩展接口采集并落盘性能数据"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0134.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0134.html"
---

# 使用msproftx扩展接口采集并落盘性能数据

为了获取用户和上层框架程序的性能数据，Profiling开启msproftx功能之前，需要在程序内调用msproftx相关接口来对用户程序进行打点以输出对应的性能数据。

#### API简介
**表1**API简介
接口

说明

acl.prof.create_stamp

创建msproftx事件标记，用于描述瞬时事件。

acl.prof.set_stamp_trace_message

为msproftx事件标记携带描述信息，在Profiling解析结果中msprof_tx summary数据展示。

acl.prof.mark

msproftx标记瞬时事件。

acl.prof.push

msproftx用于记录事件发生的时间跨度的开始时间。与acl.prof.pop成对使用，仅能在单线程内使用。

acl.prof.pop

msproftx用于记录事件发生的时间跨度的结束时间。与acl.prof.push成对使用，仅能在单线程内使用。

acl.prof.range_start

msproftx用于记录事件发生的时间跨度的开始时间。与acl.prof.range_stop成对使用，可跨线程使用。

acl.prof.range_stop

msproftx用于记录事件发生的时间跨度的结束时间。与acl.prof.range_start成对使用，可跨线程使用。

acl.prof.destroy_stamp

释放msproftx事件标记。
|  |  |
| --- | --- |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |

#### API调用示例

Profiling msproftx接口，如下示例代码。

- 示例一
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
```

```
for i in range(200000):
    stamp = acl.prof.create_stamp()
    if stamp == 0:
        print("stamp is nullptr")
        return FAILED

    msg = "test msprof tx"
    msg_len = len(msg)
    ret = acl.prof.set_stamp_trace_message(stamp, msg, msg_len)
    ret = acl.prof.mark(stamp)

    ret = acl.prof.destroy_stamp(stamp)

```
|  |  |
| --- | --- |

- 示例二
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
```

```
for i in range(200000):
    stamp = acl.prof.create_stamp()
    if stamp == 0:
        print("stamp is nullptr")
        return FAILED

    msg = "test msprof tx"
    msg_len = len(msg)
    ret = acl.prof.set_stamp_trace_message(stamp, msg, msg_len)

# acl.prof.push和acl.prof.pop接口配对使用，完成单线程采集
    ret = acl.prof.push(stamp)
    ret = acl.prof.pop()

    ret = acl.prof.destroy_stamp(stamp)

```
|  |  |
| --- | --- |

- 示例三
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
for i in range(200000):
    stamp = acl.prof.create_stamp()
    if stamp == 0:
        print("stamp is nullptr")
        return FAILED

    msg = "test msprof tx"
    msg_len = len(msg)
    ret = acl.prof.set_stamp_trace_message(stamp, msg, msg_len)

# acl.prof.range_start和acl.prof.range_stop接口配对使用，可以完成多线程采集
    range_id = 0
    range_id, ret = acl.prof.range_start(stamp)
    ret = acl.prof.range_stop(range_id)

    ret = acl.prof.destroy_stamp(stamp)

```
|  |  |
| --- | --- |


msproftx扩展接口在main函数内调用。
**父主题：**[使用acl Python接口采集性能数据](atlasprofiling_16_0131.html)