---
title: "Communication部分设计文档"
source: "msinsight-docs://zh/design_documents/Communication.md"
date_collected: "2026-05-04"
category: "design_documents"
original_path: "zh/design_documents/Communication.md"
---

# Communication部分设计文档 

## 接口与数据映射关系

### 原始数据（ATT处理后文件）

#### text场景

![image](images/communication_text_data.png)

#### db场景



### 处理后db数据内容

#### text场景

![image](images/communication_processed_text_data.png)

#### db场景

![image](images/communication_processed_db_data.png)

| 页面数据 | URL请求 | db数据类型 | text数据类型 |
| --- | --- | --- | --- |
| ![image](images/communication_page_data_1.png) | communication/matrix/bandwidthInfo | ![image](images/communication_db_data_1.png) | ![image](images/communication_text_data_1_1.png)  |
| ![image](images/communication_duration_iterations_1.png) | communication/duration/iterations | ![image](images/communication_duration_iterations_2.png) | ![image](images/communication_duration_iterations_3.png) |
| ![image](images/communication_matrix_group_1.png) | communication/matrix/group | ![image](images/communication_matrix_group_2.png) | ![image](images/communication_matrix_group_3.png) 底层数据来源于：![image](images/communication_matrix_group_4.png) |
| ![image](images/communication_sortOpNames_1.png) | communication/matrix/sortOpNames |  | ![image](images/communication_sortOpNames_2.png) 底层数据：![image](images/communication_sortOpNames_3.png) |
| ![image](images/communication_operatorNames_1.png) | communication/duration/operatorNames | ![image](images/communication_operatorNames_2.png) | ![image](images/communication_operatorNames_3.png) 数据： ![image](images/communication_operatorNames_5.png)![image](images/communication_operatorNames_6.png)|
| ![image](images/communication_operatorLists_1.png) | communication/operatorLists | ![image](images/communication_operatorLists_2.png) | ![image](images/communication_operatorLists_3.png) 数据： |
| ![image](images/communication_duration_list_1.png) | communication/duration/list | ![image](images/communication_duration_list_2.png)专家建议是由以上数据计算得到 | ![image](images/communication_duration_list_3.png) ![image](images/communication_duration_list_4.png)|
| ![image](images/communication_operatorDetails_1.png) | communication/operatorDetails | ![image](images/communication_operatorDetails_2.png) | ![image](images/communication_operatorDetails_3.png) |
| ![image](images/communication_distribution_1.png) | communication/distribution | ![image](images/communication_distribution_2.png) | ![image](images/communication_distribution_3.png) |
| ![image](images/communication_bandwidth_1.png) | communication/bandwidth | ![image](images/communication_bandwidth_2.png) | ![image](images/communication_bandwidth_3.png) |
