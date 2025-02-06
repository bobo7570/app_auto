# 移动端自动化测试平台

这是一个基于Python的移动端自动化测试平台，支持iOS和Android设备的自动化测试。

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
├── assets/           # 资源文件
├── config/           # 配置文件
├── pages/           # 页面对象
├── test_cases/      # 测试用例
├── test_data/       # 测试数据
├── utils/           # 工具类
├── web_ui/          # GUI界面
└── requirements.txt # 依赖包
```

## 贡献指南

欢迎提交Issue和Pull Request来帮助改进项目。

## 许可证

MIT License