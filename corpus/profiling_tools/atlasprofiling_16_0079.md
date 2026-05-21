---
title: "宏定义"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0079.html"
date_collected: "2026-05-04"
category: "profiling_tools"
original_path: "zh/mindstudio/830/T&ITools/Profiling/atlasprofiling_16_0079.html"
---

# 宏定义

- PROF：将采集语句封装起来，这样可以通过ENABLE_PROF宏定义在编译期间控制是否采集数据，支持传入一个参数或者两个参数。
  - 一个参数：采集语句。
当定义ENABLE_PROF会正常执行打印，当没有定义则不会打印。

**PROF(std::cout<<****"enable prof" <<**std::endl);

  - 两个参数：采集级别，采集语句。自动初始化采集类以及定义采集级别。
当定义ENABLE_PROF会正常执行采集，当没有定义则不会采集，会自动初始化Profiler类。

PROF(INFO, Attr("req", 1).Event("recv"));

- ENABLE_PROF：与PROF协同使用，当没有定义该环境变量，说明不开启采集能力，会自动将PROF定义为空实现。通常定义在CMakeLists.txt中。
add_definitions(-DENABLE_PROF)

**父主题：**[服务化调优](atlasprofiling_16_0059.html)