# 试卷分割系统 - 功能模块文档

## 项目概述

本项目实现初高中试卷的自动分割功能，支持将整卷PDF/图片按题目分割为独立文件，便于学生按题作答和复习。

## 目录结构

```
pdf_to_cn/
├── src/                    # 源代码目录
├── config/                 # 配置文件目录
├── tests/                  # 测试目录
├── docs/                   # 文档目录
└── requirements.txt        # 依赖清单
```

## 功能模块

### 1. PDF处理模块

**依赖**: `PyMuPDF>=1.23.0`, `pdf2image>=1.16.0`

**功能说明**:
- 加载PDF文件
- 提取PDF页面为图像
- 获取页面尺寸和布局信息
- 支持多页试卷批量处理

**主要接口**:
- `load_pdf()` - 加载PDF文件
- `pdf_to_images()` - 将PDF页面转换为图像

---

### 2. 图像处理模块

**依赖**: `opencv-python>=4.8.0`, `numpy>=1.24.0`, `Pillow>=10.0.0`

**功能说明**:
- 图像灰度化与二值化
- 去噪处理
- 对比度增强
- 图像裁剪与缩放

**主要接口**:
- `preprocess_image()` - 图像预处理
- `binarize()` - 二值化处理
- `denoise()` - 去噪处理

---

### 3. 题目检测模块

**依赖**: `pytesseract>=0.3.10`

**功能说明**:
- 检测试卷中的题目序号（如：1、2、3或一、二、三）
- 识别大题标题（如：选择题、填空题、解答题）
- 定位题目边界区域
- 支持密铺试卷和答题卡分离

**主要接口**:
- `detect_questions()` - 检测所有题目位置
- `detect_section_headers()` - 检测大题标题
- `get_question_regions()` - 获取题目区域坐标

---

### 4. 分割输出模块

**功能说明**:
- 按题目区域裁剪图像
- 生成独立题目文件
- 支持多种输出格式（PNG、JPG、PDF）
- 批量输出到指定目录

**主要接口**:
- `split_by_questions()` - 按题目分割
- `save_question_image()` - 保存单题图像
- `export_questions()` - 批量导出

---

## 目录结构规划（待实现）

```
src/
├── pdf_processor.py    # PDF处理模块
├── image_processor.py  # 图像处理模块
├── question_detector.py # 题目检测模块
├── splitter.py          # 分割输出模块
└── main.py              # 主程序入口
```

## 开发指南

### 环境配置

```bash
# 创建虚拟环境
python -m venv venv

# 安装依赖
pip install -r requirements.txt

# 配置Tesseract OCR
# Windows: 下载安装包并添加到PATH
# Linux: sudo apt install tesseract-ocr
```

### 运行测试

```bash
pytest tests/
```
