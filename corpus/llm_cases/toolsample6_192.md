---
title: "NCS调优"
source: "https://www.hiascend.com/document/detail/zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_192.html"
date_collected: "2026-05-04"
category: "llm_cases"
original_path: "zh/mindstudio/830/practicalcases/GeneralPerformanceIssue/toolsample6_192.html"
---

# NCS调优

对于部分运行在RC模式的产品，产品普遍存在内存较小的特点。这就导致了模型无法通过本地AOE进行调优，这样就需要用到另一种调优方式，NCS调优。

#### 安装CANN包

- 环境准备
[一台常规的Linux服务器（后文描述为Host机）和一台装有昇腾NPU的服务器（后文描述为Device机）。服务器上需要安装toolkit包，以CANN 8.0.0版本为例，toolkit包的安装方法参考对应版本的CANN安装指南](https://www.hiascend.com/document/detail/zh/canncommercial/82RC1/softwareinst/instg/instg_0008.html?Mode=PmIns&InstallType=local&OS=Ubuntu&Software=cannToolKit)。
**图1**
环境准备
- 配置环境变量
  - Host机
***加载CANN安装路径的环境变量脚本set_env.sh, CANN安装路径以${****install_path****}***为例。
************
```
source ${install_path}/ascend-toolkit/set_env.sh
```

  - Device机
```
export LD_LIBRARY_PATH=${install_path}/latest/tools/ncs/lib64/:${install_path}/latest/runtime/lib64/:$LD_LIBRARY_PATH
exportPATH=${install_path}/latest/tools/ncs/bin/:$PATH
```

其中install_path请配置为CANN软件的实际安装路径。

#### 配置密钥证书

请先确认Host机和Device机处于同一主网段，可以互相ping通。

1. 在Host机中上传shell脚本，脚本如下：

```
DEVICE_IP=10.x.x.196   # your device ip
HOST_IP=10.x.x.66 # your host IP
PASS_PHRASE=Ncx12345 # yourpassphrase
KEY_LEN=3072 # [3072,4096]
VALID_DAYS=365 # thecertwillexpireafterthevaliddays
COUNTRY=CN # yourcountrynameabbr.(2lettercode)
STATE=Zhejiang # yourprovincename
LOCATION=Hangzhou # yourcityname
ORGANIZATION=ABC # yourcompanyname
ORGANIZATION_UNIT=DEF # yoursectionname
COMMON_NAME_ROOT=www.aoe.com # yourdomainname
ENCRYPT_MODE=aes256 # [aes256,aes128]

##########该分割线以上内容请根据实际情况修改，以下内容不建议修改。##########

# generateconf
rm-rfhost-ext.cnfdevice-ext.cnf
echo"[ext]">>host-ext.cnf
echo"subjectAltName=IP:${HOST_IP}">>host-ext.cnf
echo"[ext]">>device-ext.cnf
echo"subjectAltName=IP:${DEVICE_IP}">>device-ext.cnf

# generaterootcert
opensslreq-x509-newkeyrsa:${KEY_LEN}-days${VALID_DAYS}-nodes-keyoutca-key.pem-outca-cert.pem-subj"/C=${COUNTRY}/ST=${STATE}/L=${LOCATION}/O=${ORGANIZATION}/OU=${ORGANIZATION_UNIT}/CN=${COMMON_NAME_ROOT}"-addextkeyUsage=keyCertSign

# generatedevicecertrequest
opensslreq-newkeyrsa:${KEY_LEN}-nodes-keyoutdevice-key.pem-outdevice-cert.csr-subj"/C=${COUNTRY}/ST=${STATE}/L=${LOCATION}/O=${ORGANIZATION}/OU=${ORGANIZATION_UNIT}/CN=NCS"
# generatedevicecert
opensslx509-req-indevice-cert.csr-days${VALID_DAYS}-CAca-cert.pem-CAkeyca-key.pem-CAcreateserial-outdevice-cert.pem-extensionsext-extfiledevice-ext.cnf

# generatehostcertrequest
opensslreq-newkeyrsa:${KEY_LEN}-nodes-keyouthost-key.pem-outhost-cert.csr-subj"/C=${COUNTRY}/ST=${STATE}/L=${LOCATION}/O=${ORGANIZATION}/OU=${ORGANIZATION_UNIT}/CN=NCA"
# generatehostcert
opensslx509-req-inhost-cert.csr-days${VALID_DAYS}-CAca-cert.pem-CAkeyca-key.pem-CAcreateserial-outhost-cert.pem-extensionsext-extfilehost-ext.cnf

# encrytprivatekey
opensslrsa-inhost-key.pem-passoutpass:${PASS_PHRASE}-${ENCRYPT_MODE}-outhost-key.pem
opensslrsa-indevice-key.pem-passoutpass:${PASS_PHRASE}-${ENCRYPT_MODE}-outdevice-key.pem
```

2. 将Device Ip和Host Ip改成对应的ip地址，在Host机上运行该shell脚本，生成密钥证书文件。
**表1**相关文件说明
文件名

作用

ca-cert.pem

根CA，需要拷贝到开发环境和运行环境上。

host-key.pem

开发环境端私钥，需要拷贝到开发环境上。

host-cert.pem

开发环境端证书，需要拷贝到开发环境上。

device-key.pem

运行环境端私钥，需要拷贝到运行环境上。

device-cert.pem

运行环境端证书，需要拷贝到运行环境上。

ca-key.pem

中间过程文件，可忽略。

ca-cert.srl

中间过程文件，可忽略。

host-cert.csr

中间过程文件，可忽略。

device-cert.csr

中间过程文件，可忽略。

host-ext.cnf

中间过程文件，可忽略。

device-ext.cnf

中间过程文件，可忽略。
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
|  |  |
|  |  |
|  |  |

3. 将device-key.pem 、device-cert.pem和ca-cert.pem三个文件拷贝到Device机上，在密钥证书所在路径执行如下命令。

  - Host机
```
akt --private_key host-key.pem --public_cert host-cert.pem --ca_cert ca-cert.pem
```

  - Device机
```
akt --private_key device-key.pem --public_cert device-cert.pem --ca_cert ca-cert.pem
```

示例命令中的私钥文件名为：host-key.pem或者device-key.pem，设备证书文件名为：host-cert.pem或者device-cert.pem，根证书文件名为：ca-cert.pem。

4. 执行命令后，提示“Enter Password:”，请输入加密私钥的口令PASS_PHRASE（口令必须与生成私钥时的口令一致）。
回显如下，表示证书导入成功。
```
Load cert, password, and key successfully.
```

#### 执行调优

1. AOE调优前，在Host机上，使用如下命令可选配置部分环境。

```
export TUNE_BANK_PATH={bank_path}  # 指定知识库保存地址

export TE_PARALLEL_COMPILER=32     # 加速aoe调优
```

2. 执行以下命令，使用AOE调优。

Device机侧：

```
ncs &
```
执行后查询NCS是否启动成功。
```
ps -ef|grep ncs|grep -v "grep"
```

回显信息如下所示，代表NCS服务启动成功。ID为257435的进程是ncs守护进程，ID为257440的进程是ncs运行进程。

```
root257440257435007:54pts/300:00:01ncs--ipXX.XX.XX.XX--portXXXX--daemonfalse
```

Host机侧：

```
aoe --framework 5 --model ./model.onnx --output model --job_type 2 --ip xx.xx.xx.xx --aicore_num=1
```

命令中的参数说明如表2[所示。更多调优参数可以参考《AOE调优工具用户指南](https://www.hiascend.com/document/detail/zh/canncommercial/850/devaids/aoe/auxiliarydevtool_aoe_0001.html)》。
**表2**参数说明
参数

说明

--model

需要调优的模型。

--output

调优完成的模型的保存名字。

--job_type

子图调优或者算子调优，分别是2和1，需要先进行子图调优，再进行算子调优，先后执行一遍。

--ip

Device机的Ip地址。

--aicore_num

AI Core数量。
|  |  |
| --- | --- |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |

3. 命令执行后，会有打印提示性能优化的比例，如图2所示，性能优化提升53%。
**图2**
调优回显

**父主题：**[ONNX模型调优](toolsample6_096.html)