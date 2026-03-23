# 试卷分割系统 - API 文档

## 目录

1. [PDF处理模块](#一pdf处理模块)
2. [图像处理模块](#二图像处理模块)
3. [题目检测模块](#三题目检测模块)
4. [分割输出模块](#四分割输出模块)
5. [配置模块](#五配置模块)
6. [主程序接口](#六主程序接口)

---

## 一、PDF处理模块

**模块路径**: `src.pdf_processor`

**导入方式**:
```python
from src.pdf_processor import PDFProcessor
```

### 类: `PDFProcessor`

#### 构造函数

```python
PDFProcessor(file_path: str = None)
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| file_path | str | 否 | PDF文件路径 |

**示例**:
```python
processor = PDFProcessor("test.pdf")
```

---

#### `load()`

加载PDF文件。

```python
def load(self, file_path: str) -> bool
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| file_path | str | 是 | PDF文件路径 |

**返回**: `bool` - 加载是否成功

---

#### `get_page_count()`

获取PDF页数。

```python
def get_page_count(self) -> int
```

**返回**: `int` - 页面总数

---

#### `get_page_info()`

获取指定页面信息。

```python
def get_page_info(self, page_num: int) -> dict
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| page_num | int | 是 | 页码（从1开始） |

**返回**: `dict`
```python
{
    "page_num": int,      # 页码
    "width": float,       # 页面宽度(像素)
    "height": float,      # 页面高度(像素)
    "rotation": int       # 旋转角度
}
```

---

#### `pdf_to_images()`

将PDF页面转换为图像。

```python
def pdf_to_images(self,
                  dpi: int = 300,
                  first_page: int = None,
                  last_page: int = None) -> List[np.ndarray]
```

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| dpi | int | 否 | 300 | 输出图像DPI |
| first_page | int | 否 | None | 起始页（None=首页） |
| last_page | int | 否 | None | 结束页（None=末页） |

**返回**: `List[np.ndarray]` - 图像数组列表

---

#### `save_page_as_image()`

保存指定页面为图像文件。

```python
def save_page_as_image(self,
                       page_num: int,
                       output_path: str,
                       dpi: int = 300,
                       format: str = "PNG") -> bool
```

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| page_num | int | 是 | - | 页码 |
| output_path | str | 是 | - | 输出文件路径 |
| dpi | int | 否 | 300 | 图像DPI |
| format | str | 否 | "PNG" | 输出格式 (PNG/JPG) |

**返回**: `bool` - 保存是否成功

---

[⬆ 返回目录](#目录)

---

## 二、图像处理模块

**模块路径**: `src.image_processor`

**导入方式**:
```python
from src.image_processor import ImageProcessor
```

### 类: `ImageProcessor`

#### 构造函数

```python
ImageProcessor(image: np.ndarray = None)
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| image | np.ndarray | 否 | 输入图像 |

---

#### `load()`

加载图像文件。

```python
def load(self, image_path: str) -> np.ndarray
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| image_path | str | 是 | 图像文件路径 |

**返回**: `np.ndarray` - 图像数组

---

#### `preprocess()`

图像预处理（灰度化+二值化+去噪）。

```python
def preprocess(self,
               binarize: bool = True,
               denoise: bool = True,
               enhance: bool = True) -> np.ndarray
```

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| binarize | bool | 否 | True | 是否二值化 |
| denoise | bool | 否 | True | 是否去噪 |
| enhance | bool | 否 | True | 是否增强对比度 |

**返回**: `np.ndarray` - 处理后的图像

---

#### `binarize()`

图像二值化。

```python
def binarize(self, threshold: int = 127) -> np.ndarray
```

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| threshold | int | 否 | 127 | 二值化阈值 (0-255) |

**返回**: `np.ndarray` - 二值化后的图像

---

#### `denoise()`

图像去噪。

```python
def denoise(self, method: str = "gaussian") -> np.ndarray
```

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| method | str | 否 | "gaussian" | 去噪方法 (gaussian/median/bilateral) |

**返回**: `np.ndarray` - 去噪后的图像

---

#### `enhance_contrast()`

增强对比度。

```python
def enhance_contrast(self, alpha: float = 1.5, beta: int = 0) -> np.ndarray
```

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| alpha | float | 否 | 1.5 | 对比度系数 |
| beta | int | 否 | 0 | 亮度调整值 |

**返回**: `np.ndarray` - 增强后的图像

---

#### `crop()`

裁剪图像区域。

```python
def crop(self, x: int, y: int, width: int, height: int) -> np.ndarray
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| x | int | 是 | 左上角X坐标 |
| y | int | 是 | 左上角Y坐标 |
| width | int | 是 | 裁剪宽度 |
| height | int | 是 | 裁剪高度 |

**返回**: `np.ndarray` - 裁剪后的图像

---

#### `resize()`

调整图像大小。

```python
def resize(self, width: int = None, height: int = None,
           scale: float = None) -> np.ndarray
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| width | int | 否 | 目标宽度 |
| height | int | 否 | 目标高度 |
| scale | float | 否 | 缩放比例 |

**返回**: `np.ndarray` - 调整后的图像

---

#### `save()`

保存图像到文件。

```python
def save(self, output_path: str, format: str = "PNG") -> bool
```

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| output_path | str | 是 | - | 输出文件路径 |
| format | str | 否 | "PNG" | 输出格式 |

**返回**: `bool` - 保存是否成功

---

[⬆ 返回目录](#目录)

---

## 三、题目检测模块

**模块路径**: `src.question_detector`

**导入方式**:
```python
from src.question_detector import QuestionDetector
```

### 类: `QuestionDetector`

#### 构造函数

```python
QuestionDetector(config: dict = None)
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| config | dict | 否 | 检测配置参数 |

**config 默认值**:
```python
{
    "min_question_height": 20,      # 最小题目高度(像素)
    "question_number_patterns": [   # 题目序号匹配模式
        r"^\d+[.、]",               # 阿拉伯数字: 1. 2、
        r"^[一二三四五六七八九十]+[.、]",  # 中文数字
    ],
    "section_patterns": [           # 大题标题匹配模式
        r"^选择题$",
        r"^填空题$",
        r"^解答题$",
    ],
    "ocr_lang": "chi_sim+eng",       # OCR语言
}
```

---

#### `detect_questions()`

检测图像中的所有题目位置。

```python
def detect_questions(self, image: np.ndarray) -> List[dict]
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| image | np.ndarray | 是 | 输入图像 |

**返回**: `List[dict]` - 题目位置列表
```python
[
    {
        "id": int,           # 题目编号
        "type": str,         # "question" / "section"
        "number": str,       # 题目序号文本
        "bbox": (x, y, w, h), # 边界框
        "text": str,         # 识别文本
    },
    ...
]
```

---

#### `detect_section_headers()`

检测大题标题区域。

```python
def detect_section_headers(self, image: np.ndarray) -> List[dict]
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| image | np.ndarray | 是 | 输入图像 |

**返回**: `List[dict]` - 大题标题列表
```python
[
    {
        "type": str,         # 标题类型
        "bbox": (x, y, w, h),
        "text": str,
    },
    ...
]
```

---

#### `get_question_regions()`

获取所有题目的区域坐标。

```python
def get_question_regions(self, image: np.ndarray,
                         include_answer_area: bool = True) -> List[tuple]
```

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| image | np.ndarray | 是 | - | 输入图像 |
| include_answer_area | bool | 否 | True | 是否包含答题区域 |

**返回**: `List[tuple]` - 区域坐标列表 `[(x, y, w, h), ...]`

---

#### `detect_answer_area()`

检测答题区域。

```python
def detect_answer_area(self, image: np.ndarray,
                       question_bbox: tuple) -> tuple
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| image | np.ndarray | 是 | 输入图像 |
| question_bbox | tuple | 是 | 题目边界框 (x, y, w, h) |

**返回**: `tuple` - 答题区域坐标 (x, y, w, h)

---

[⬆ 返回目录](#目录)

---

## 四、分割输出模块

**模块路径**: `src.splitter`

**导入方式**:
```python
from src.splitter import Splitter
```

### 类: `Splitter`

#### 构造函数

```python
Splitter(output_dir: str = "./output")
```

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| output_dir | str | 否 | "./output" | 输出目录 |

---

#### `split_by_questions()`

按题目分割图像。

```python
def split_by_questions(self,
                       image: np.ndarray,
                       regions: List[tuple],
                       question_numbers: List[str] = None) -> List[np.ndarray]
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| image | np.ndarray | 是 | 输入图像 |
| regions | List[tuple] | 是 | 题目区域列表 |
| question_numbers | List[str] | 否 | 题目编号列表 |

**返回**: `List[np.ndarray]` - 分割后的图像列表

---

#### `save_question()`

保存单题图像。

```python
def save_question(self,
                  image: np.ndarray,
                  question_id: int,
                  output_dir: str = None,
                  format: str = "PNG",
                  prefix: str = "Q") -> str
```

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| image | np.ndarray | 是 | - | 题目图像 |
| question_id | int | 是 | - | 题目编号 |
| output_dir | str | 否 | 构造器指定 | 输出目录 |
| format | str | 否 | "PNG" | 输出格式 |
| prefix | str | 否 | "Q" | 文件名前缀 |

**返回**: `str` - 保存的文件路径

---

#### `export_questions()`

批量导出所有题目。

```python
def export_questions(self,
                     images: List[np.ndarray],
                     question_ids: List[int] = None,
                     output_dir: str = None,
                     format: str = "PNG",
                     prefix: str = "Q") -> List[str]
```

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| images | List[np.ndarray] | 是 | - | 题目图像列表 |
| question_ids | List[int] | 否 | None | 题目编号列表 |
| output_dir | str | 否 | 构造器指定 | 输出目录 |
| format | str | 否 | "PNG" | 输出格式 |
| prefix | str | 否 | "Q" | 文件名前缀 |

**返回**: `List[str]` - 保存的文件路径列表

---

#### `export_to_pdf()`

导出为PDF文件。

```python
def export_to_pdf(self,
                  images: List[np.ndarray],
                  output_path: str,
                  question_ids: List[int] = None) -> bool
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| images | List[np.ndarray] | 是 | 题目图像列表 |
| output_path | str | 是 | 输出PDF路径 |
| question_ids | List[int] | 否 | 题目编号列表 |

**返回**: `bool` - 导出是否成功

---

[⬆ 返回目录](#目录)

---

## 五、配置模块

**模块路径**: `src.config`

**导入方式**:
```python
from src.config import Config
```

### 类: `Config`

#### 加载配置

```python
Config.load(config_path: str = None) -> dict
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| config_path | str | 否 | 配置文件路径 |

**返回**: `dict` - 配置字典

---

#### 获取配置项

```python
Config.get(key: str, default: any = None) -> any
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| key | str | 是 | 配置键名 |
| default | any | 否 | 默认值 |

**返回**: `any` - 配置值

---

[⬆ 返回目录](#目录)

---

## 六、主程序接口

**模块路径**: `src.main`

**导入方式**:
```python
from src.main import PaperSplitterApp
```

### 类: `PaperSplitterApp`

#### 构造函数

```python
PaperSplitterApp()
```

---

#### `run()`

启动应用程序。

```python
def run(self)
```

---

#### `process_file()`

处理单个试卷文件。

```python
def process_file(self,
                 file_path: str,
                 output_dir: str = None,
                 output_format: str = "PNG",
                 dpi: int = 300) -> dict
```

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| file_path | str | 是 | - | 输入文件路径 |
| output_dir | str | 否 | None | 输出目录 |
| output_format | str | 否 | "PNG" | 输出格式 |
| dpi | int | 否 | 300 | 图像DPI |

**返回**: `dict` - 处理结果
```python
{
    "success": bool,              # 处理是否成功
    "total_questions": int,       # 题目总数
    "output_files": List[str],    # 输出文件列表
    "errors": List[str],          # 错误信息列表
}
```

---

#### `batch_process()`

批量处理多个文件。

```python
def batch_process(self,
                 file_paths: List[str],
                 output_dir: str = None,
                 output_format: str = "PNG",
                 dpi: int = 300) -> List[dict]
```

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| file_paths | List[str] | 是 | - | 输入文件路径列表 |
| output_dir | str | 否 | None | 输出目录 |
| output_format | str | 否 | "PNG" | 输出格式 |
| dpi | int | 否 | 300 | 图像DPI |

**返回**: `List[dict]` - 各文件处理结果列表

---

[⬆ 返回目录](#目录)

---

## 异常类

| 异常类 | 说明 |
|--------|------|
| `PDFLoadError` | PDF加载失败 |
| `ImageProcessError` | 图像处理失败 |
| `QuestionDetectError` | 题目检测失败 |
| `ExportError` | 导出失败 |

---

## 使用示例

```python
from src.pdf_processor import PDFProcessor
from src.image_processor import ImageProcessor
from src.question_detector import QuestionDetector
from src.splitter import Splitter
from src.main import PaperSplitterApp

# 方式一：分步处理
processor = PDFProcessor("test.pdf")
images = processor.pdf_to_images(dpi=300)

img_proc = ImageProcessor(images[0])
processed = img_proc.preprocess()

detector = QuestionDetector()
regions = detector.get_question_regions(processed)

splitter = Splitter("./output")
result = splitter.export_questions([processed], [1])

# 方式二：使用主程序一键处理
app = PaperSplitterApp()
result = app.process_file("test.pdf", output_dir="./output")
```
