---
title: "算子使用"-O0 -g"编译选项编译后，运行出错，"min stack size is xxx, larger than current process default size 32768. Please modify aclInit json, and reboot process.""
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0145.html"
date_collected: "2026-05-04"
category: "operator_tools"
original_path: "zh/mindstudio/830/ODtools/Operatordevelopmenttools/atlasopdev_16_0145.html"
---

# 算子使用"-O0 -g"编译选项编译后，运行出错，"min stack size is xxx, larger than current process default size 32768. Please modify aclInit json, and reboot process."

#### 现象描述

算子使用"-O0 -g"编译选项编译后，运行出错，出现以下报错。

```
[ERROR] xxx min stack size is xxx, larger than current process default size 32768. Please modify aclInit json, and reboot process.
```

#### 原因分析

出现该错误代表核函数使用的栈空间过大，超过了当前进程默认配置的栈空间大小，算子注册失败。

#### 解决措施
[参考AI Core栈空间大小配置示例](https://www.hiascend.com/document/detail/zh/canncommercial/83RC1/API/appdevgapi/aclcppdevg_03_0022.html#ZH-CN_TOPIC_0000002446511118__section161115349403)，在aclInit()接口传入的json文件中，配置更大的栈空间，比如在json文件中增加如下配置，扩大栈空间大小至65536字节：
```
{   
      "StackSize":{
            "aicore_stack_size":65536   
      } 
}
```
**父主题：**[FAQ](atlasopdev_16_0077.html)