# 试卷分割系统

将初高中试卷PDF按题目自动分割为独立文件的工具。

## 功能特点

- 支持 PDF 和图片格式输入
- 自动检测题目序号（阿拉伯数字/中文数字）
- 识别大题标题（选择题、填空题、解答题）
- 多种输出格式（PNG、JPG、PDF）
- 批量处理能力

## 环境要求

- Python 3.8+
- Tesseract OCR

## 安装

### 1. 克隆项目

```bash
cd paper_splitter
```

### 2. 创建虚拟环境

```bash
python -m venv venv
source venv/Scripts/activate  # Windows
# source venv/bin/activate    # Linux/Mac
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 安装 Tesseract OCR

**Windows**:
1. 下载 [Tesseract 安装包](https://github.com/UB-Mannheim/tesseract/wiki)
2. 安装并添加到系统 PATH
3. 安装中文语言包

**Linux**:
```bash
sudo apt install tesseract-ocr tesseract-ocr-chi-sim
```

**Mac**:
```bash
brew install tesseract tesseract-lang
```

## 快速开始

### Python API

```python
from src.main import PaperSplitterApp

app = PaperSplitterApp()
result = app.process_file("test.pdf", output_dir="./output")
print(f"分割完成，共 {result['total_questions']} 题")
```

### 命令行

```bash
python -m src.main input.pdf -o ./output --format png --dpi 300
```

## 项目结构

```
paper_splitter/
├── src/                # 源代码
├── config/             # 配置文件
├── tests/              # 测试文件
├── docs/               # 文档
├── requirements.txt    # 依赖清单
└── README.md
```

## 文档

- [API文档](docs/api.md)
- [使用手册](docs/使用手册.md)
- [开发指南](docs/开发指南.md)
- [配置说明](docs/配置说明.md)
- [里程碑](docs/milestones.md)

## 许可证

MIT License
