# 智能螺杆泵诊断系统

## 1. screwai 主程序
  
- config 配置信息
  - config.yaml 主要配置文件

- core 核心函数代码文件夹
  - base.py 基础函数包
  - config.py 配置文件加载包
  - database.py 涉及数据库函数包
  - domain.py 专业知识函数包
  - draw_effici.py 泵效绘图函数包
  - split_section.py 泵效区间划分函数包

- data_analysis 数据分析
  - d1_info_statistics.py 宏观控制图前置数据分析步骤

- fault_diagnosis 故障诊断相关程序

- macro_control 宏观示功图相关程序
  - m2_macro_control.py 宏观控制图

- web_page dash框架页面
- screwai_app.py dash框架软件启动程序

- *test.py 测试文件，可删除



- structure.md 程序结构说明文件


## 2. data_dir 数据总文件夹

- 重要数据 人工处理的重要数据保存路径，不可删除内容
- info_save 程序生成的数据保存路径








