# 移动端自动化测试平台

这是一个基于Python的移动端自动化测试平台，支持iOS和Android设备的自动化测试。采用Page Object设计模式，支持多设备管理，提供美观的GUI界面。

## 功能特点

- 支持iOS和Android平台
- 美观的图形用户界面
- 灵活的测试用例管理
- 实时设备检测
- 自动化测试执行
- 测试报告生成与查看

## 环境要求

- Python 3.7+
- Appium Server
- iOS/Android SDK
- 相关依赖包（见requirements.txt）

## 安装步骤

1. 克隆仓库
```bash
git clone https://github.com/bobo7570/app_auto.git
cd app_auto
```

2. 创建并激活虚拟环境
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. 安装依赖
```bash
pip install -r requirements.txt
```

4. 配置设备信息
- 编辑 config/config.yaml 文件
- 配置设备信息和测试环境

## 使用说明

1. 启动GUI界面
```bash
python web_ui/main.py
```

2. 在GUI界面中：
- 选择测试平台（iOS/Android）
- 选择测试设备
- 选择要执行的测试用例
- 点击"开始测试"按钮执行测试
- 测试完成后可查看测试报告

## 项目结构

```
app_auto/
├── assets/           # 资源文件目录
│   ├── folder.png    # 文件夹图标
│   └── file.png      # 文件图标
│
├── config/           # 配置文件目录
│   ├── config.yaml   # 主配置文件（设备、环境配置）
│   └── locators.yaml # 元素定位配置文件
│
├── pages/           # 页面对象目录（Page Object模式）
│   ├── base_page.py # 基础页面类
│   └── login_page.py # 登录页面类
│
├── test_cases/      # 测试用例目录
│   ├── community/   # 社区相关测试
│   │   └── test_post.py
│   ├── friends/     # 好友相关测试
│   │   ├── conftest.py
│   │   └── test_add_friend.py
│   └── test_login.py # 登录测试
│
├── test_data/       # 测试数据目录
│   └── friends_data.yaml # 好友测试数据
│
├── utils/           # 工具类目录
│   ├── device_manager.py # 设备管理工具
│   ├── driver.py    # Appium驱动管理
│   └── logger.py    # 日志工具
│
├── web_ui/          # GUI界面目录
│   └── main.py      # 主界面程序
│
├── requirements.txt # 项目依赖
├── conftest.py      # Pytest配置文件
└── README.md        # 项目说明文档
```

## 目录说明

### assets/
存放项目资源文件，如图标、图片等静态资源。

### config/
配置文件目录：
- config.yaml：主配置文件，包含设备信息、环境配置等
- locators.yaml：元素定位配置，存储页面元素的定位方式

### pages/
使用Page Object模式组织的页面对象目录：
- base_page.py：封装基础页面操作
- login_page.py：登录页面的元素定位和操作方法

### test_cases/
测试用例目录，按功能模块组织：
- community/：社区相关测试用例
- friends/：好友相关测试用例
- test_login.py：登录功能测试

### test_data/
测试数据目录，存放测试用例需要的测试数据文件

### utils/
工具类目录：
- device_manager.py：设备管理工具，负责设备的检测和信息获取
- driver.py：Appium驱动管理器，负责初始化和管理WebDriver
- logger.py：日志工具，统一的日志记录实现

### web_ui/
图形界面相关代码：
- main.py：主窗口实现，包含GUI布局和事件处理

## 贡献指南

欢迎提交Issue和Pull Request来帮助改进项目。提交代码时请遵循以下规范：
1. 遵循Python PEP8编码规范
2. 添加必要的注释和文档
3. 确保提交的代码已经过测试

## 许可证

MIT License