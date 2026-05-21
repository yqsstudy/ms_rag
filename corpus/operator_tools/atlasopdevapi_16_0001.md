---
title: "接口列表"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdevapi_16_0001.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdevapi_16_0001.html"
---

# 接口列表

msKPP工具分为基础功能接口和指令接口两种接口类型。基础功能接口用于模拟算子计算中芯片平台、基础数据等。指令接口用于模拟特定的算子指令操作，包括Vector类计算指令和Cube类计算指令。
**表1**msKPP工具接口列表
接口类型

接口名称

接口简介

[基础功能接口](atlasopdevapi_16_0002.html)

Chip

创建性能建模的芯片平台，初始化芯片各项性能数据。

Core

模拟芯片内部的AI Core。

Tensor

算子执行基础数据类型。

Tensor.load

数据搬运接口，对数据在不同单元搬运进行建模。

[同步类指令接口](atlasopdevapi_16_00072.html)

set_flag

核内PIPE间同步的指令接口，与wait_flag配套使用。

wait_flag

核内PIPE间同步的指令接口，与set_flag配套使用。

[指令接口](atlasopdevapi_16_00071.html)

mmad

对Cube类指令的mmad性能建模接口。

vadd

对Vector类指令的vadd性能建模接口。

vbrcb

对Vector类指令的vbrcb性能建模接口。

vconv

对Vector类指令的vconv性能建模接口。

vconv_deq

对Vector类指令的vconv_deq性能建模接口。

vconv_vdeq

对Vector类指令的vconv_vdeq性能建模接口。

vector_dup

对Vector类指令的vector_dup性能建模接口。

vexp

对Vector类指令的vexp性能建模接口。

vln

对Vector类指令的vln性能建模接口。

vmax

对Vector类指令的vmax性能建模接口。

vmul

对Vector类指令的vmul性能建模接口。

vmuls

对Vector类指令的vmuls性能建模接口。

vsub

对Vector类指令的vsub性能建模接口。

vdiv

对Vector类指令的vdiv性能建模接口。

vcadd

对Vector类指令的vcadd性能建模接口。

vabs

对Vector类指令的vabs性能建模接口。

vaddrelu

对Vector类指令的vaddrelu性能建模接口。

vaddreluconv

对Vector类指令的vaddreluconv性能建模接口。

vadds

对Vector类指令的vadds性能建模接口。

vand

对Vector类指令的vand性能建模接口。

vaxpy

对Vector类指令的vaxpy性能建模接口。

vbitsort

对Vector类指令的vbitsort性能建模接口。

vcgadd

对Vector类指令的vcgadd性能建模接口。

vcgmax

对Vector类指令的vcgmax性能建模接口。

vcgmin

对Vector类指令的vcgmin性能建模接口。

vcmax

对Vector类指令的vcmax性能建模接口。

vcmin

对Vector类指令的vcmin性能建模接口。

*vcmp_xxx*

对Vector类指令的vcmp_xxx性能建模接口。

*vcmpv_xxx*

对Vector类指令的vcmpv_xxx性能建模接口。

*vcmpvs_xxx*

对Vector类指令的vcmpvs_xxx性能建模接口。

vcopy

对Vector类指令的vcopy性能建模接口。

vcpadd

对Vector类指令的vcpadd性能建模接口。

vgather

对Vector类指令的vgather性能建模接口。

vgatherb

对Vector类指令的vgatherb性能建模接口。

vlrelu

对Vector类指令的vlrelu性能建模接口。

vmadd

对Vector类指令的vmadd性能建模接口。

vmaddrelu

对Vector类指令的vmaddrelu性能建模接口。

vmaxs

对Vector类指令的vmaxs性能建模接口。

vmin

对Vector类指令的vmin性能建模接口。

vmins

对Vector类指令的vmins性能建模接口。

vmla

对Vector类指令的vmla性能建模接口。

vmrgsort

对Vector类指令的vmrgsort性能建模接口。

vmulconv

对Vector类指令的vmulconv性能建模接口。

vnot

对Vector类指令的vnot性能建模接口。

vor

对Vector类指令的vor性能建模接口。

vrec

对Vector类指令的vrec性能建模接口。

vreduce

对Vector类指令的vreduce性能建模接口。

vreducev2

对Vector类指令的vreducev2性能建模接口。

vrelu

对Vector类指令的vrelu性能建模接口。

vrsqrt

对Vector类指令的vrsqrt性能建模接口。

vsel

对Vector类指令的vsel性能建模接口。

vshl

对Vector类指令的vshl性能建模接口。

vshr

对Vector类指令的vshr性能建模接口。

vsqrt

对Vector类指令的vsqrt性能建模接口。

vsubrelu

对Vector类指令的vsubrelu性能建模接口。

vsubreluconv

对Vector类指令的vsubreluconv性能建模接口。

vtranspose

对Vector类指令的vtranspose性能建模接口。
|  |  |  |
| --- | --- | --- |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
**父主题：**[对外接口使用说明](atlasopdev_16_0015.html)