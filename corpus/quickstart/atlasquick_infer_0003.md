---
title: "模型量化"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/msquickstart/atlasquick_infer_0003.html"
date_collected: "2026-05-04"
category: "quickstart"
original_path: "zh/mindstudio/830/msquickstart/atlasquick_infer_0003.html"
---

# 模型量化

1. 下载Llama-3.1-8B-Instruct权重和模型文件至本地，如图1[所示，单击下载](https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct)。

**图1**
![](figure/zh-cn_image_0000002502743728.png "点击放大")下载文件至本地

2. 执行以下命令，进入Llama目录。

```
cd ${HOME}/msmodelslim/example/Llama
```

其中HOME为用户自定义安装msit的路径。

3. 执行量化脚本，生成量化权重文件，并存入自定义存储路径中。示例命令为w8a16量化命令。

****
```
python3 quant_llama.py --model_path ${model_path} --save_directory ${save_directory} --device_type npu --w_bit 8 --a_bit 16 
```

[其中--model_path为已下载的模型文件所在路径；--save_directory为生成的量化权重文件的存储路径。其它模型文件量化案例可参见LLAMA量化案例](https://gitcode.com/Ascend/msmodelslim/blob/master/example/Llama/README.md#llama量化说明)。

如果量化后的权重文件需要在MindIE 2.1.RC1及之前版本上部署，需要在执行原量化命令时增加--mindie_format参数，参考命令如下：
****
```
python3 quant_llama.py --model_path ${model_path} --save_directory ${save_directory} --device_type npu --w_bit 8 --a_bit 16 --mindie_format
```

4. 量化完成后，结果图2所示，safetensors文件大小由15.1G压缩至8.5G。

**图2**
量化后的结果

5. 生成的w8a16量化权重文件如下所示。

```
├── config.json                          # 配置文件
├── generation_config.json               # 配置文件
├── quant_model_description.json         # w8a16量化后的权重描述文件
├── quant_model_weight_w8a16.safetensors # w8a16量化后的权重文件
├── tokenizer.json                       # 模型文件的tokenizer
├── tokenizer_config.json                # 模型文件的tokenizer配置文件
```

**父主题：**[模型推理](atlasquick_infer_0002.html)