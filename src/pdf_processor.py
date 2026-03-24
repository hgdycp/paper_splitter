"""
PDF处理模块 - 加载PDF并转换为图像
"""

import logging
from typing import List, Optional, Tuple

import fitz  # PyMuPDF
import numpy as np
from PIL import Image

logger = logging.getLogger(__name__)


class PDFLoadError(Exception):
    """PDF加载失败异常"""

    pass


class PDFProcessor:
    """
    PDF处理器 - 负责加载PDF并转换为图像

    Attributes:
        file_path: PDF文件路径
        _document: PyMuPDF文档对象
        _page_count: PDF页数缓存
    """

    def __init__(self, file_path: Optional[str] = None):
        """
        初始化PDF处理器。

        Args:
            file_path: PDF文件路径
        """
        self.file_path = file_path
        self._document: Optional[fitz.Document] = None
        self._page_count: Optional[int] = None

        if file_path:
            self.load(file_path)

    def load(self, file_path: str) -> bool:
        """
        加载PDF文件。

        Args:
            file_path: PDF文件路径

        Returns:
            bool: 加载是否成功

        Raises:
            PDFLoadError: PDF加载失败时抛出
        """
        try:
            self._document = fitz.open(file_path)
            self.file_path = file_path
            self._page_count = len(self._document)
            logger.info("成功加载PDF文件: %s, 页数: %d", file_path, self._page_count)
            return True
        except Exception as e:
            logger.error("PDF加载失败: %s", str(e))
            raise PDFLoadError(f"无法加载PDF文件: {file_path}, 错误: {str(e)}")

    def get_page_count(self) -> int:
        """
        获取PDF页数。

        Returns:
            int: 页面总数

        Raises:
            PDFLoadError: PDF未加载时抛出
        """
        if self._document is None:
            raise PDFLoadError("PDF文件未加载，请先调用load()方法")
        if self._page_count is None:
            self._page_count = len(self._document)
        return self._page_count

    def get_page_info(self, page_num: int) -> dict:
        """
        获取指定页面信息。

        Args:
            page_num: 页码（从1开始）

        Returns:
            dict: 页面信息字典，包含page_num、width、height、rotation

        Raises:
            PDFLoadError: PDF未加载或页码无效时抛出
        """
        if self._document is None:
            raise PDFLoadError("PDF文件未加载，请先调用load()方法")

        if page_num < 1 or page_num > self.get_page_count():
            raise PDFLoadError(f"页码无效: {page_num}, PDF共有{self.get_page_count()}页")

        page = self._document[page_num - 1]  # PyMuPDF页码从0开始
        rect = page.rect

        return {
            "page_num": page_num,
            "width": rect.width,
            "height": rect.height,
            "rotation": page.rotation,
        }

    def pdf_to_images(
        self,
        dpi: int = 300,
        first_page: Optional[int] = None,
        last_page: Optional[int] = None,
    ) -> List[np.ndarray]:
        """
        将PDF页面转换为图像列表。

        Args:
            dpi: 输出图像的分辨率，越高越清晰但处理越慢
            first_page: 起始页（None=首页）
            last_page: 结束页（None=末页）

        Returns:
            List[np.ndarray]: 图像数组列表，每元素对应一页

        Raises:
            PDFLoadError: PDF加载失败或转换失败时抛出
        """
        if self._document is None:
            raise PDFLoadError("PDF文件未加载，请先调用load()方法")

        # 计算实际页码范围
        total_pages = self.get_page_count()
        start_page = first_page if first_page is not None else 1
        end_page = last_page if last_page is not None else total_pages

        # 校验页码范围
        if start_page < 1:
            start_page = 1
        if end_page > total_pages:
            end_page = total_pages
        if start_page > end_page:
            raise PDFLoadError(f"页码范围无效: 起始页{start_page} > 结束页{end_page}")

        logger.info("开始转换PDF页面: %d-%d, DPI: %d", start_page, end_page, dpi)

        images = []
        zoom = dpi / 72  # PyMuPDF默认72 DPI
        matrix = fitz.Matrix(zoom, zoom)

        for page_num in range(start_page, end_page + 1):
            try:
                page = self._document[page_num - 1]
                pix = page.get_pixmap(matrix=matrix)

                # 转换为numpy数组 (RGB格式)
                img_data = np.frombuffer(pix.samples, dtype=np.uint8)
                img_data = img_data.reshape(pix.height, pix.width, pix.n)

                # PyMuPDF返回的是RGBA或RGB，转换为RGB
                if pix.n == 4:
                    # RGBA -> RGB
                    img_data = img_data[:, :, :3]
                elif pix.n == 1:
                    # 灰度 -> RGB
                    img_data = np.stack([img_data] * 3, axis=-1)

                images.append(img_data)
                logger.debug("转换页面 %d 成功: %dx%d", page_num, pix.width, pix.height)

            except Exception as e:
                logger.warning("转换页面 %d 失败: %s", page_num, str(e))
                continue

        logger.info("PDF转图像完成，共转换 %d 页", len(images))
        return images

    def save_page_as_image(
        self,
        page_num: int,
        output_path: str,
        dpi: int = 300,
        format: str = "PNG",
    ) -> bool:
        """
        保存指定页面为图像文件。

        Args:
            page_num: 页码（从1开始）
            output_path: 输出文件路径
            dpi: 图像DPI
            format: 输出格式 (PNG/JPG/JPEG)

        Returns:
            bool: 保存是否成功

        Raises:
            PDFLoadError: PDF未加载或页码无效时抛出
        """
        if self._document is None:
            raise PDFLoadError("PDF文件未加载，请先调用load()方法")

        if page_num < 1 or page_num > self.get_page_count():
            raise PDFLoadError(f"页码无效: {page_num}, PDF共有{self.get_page_count()}页")

        try:
            page = self._document[page_num - 1]
            zoom = dpi / 72
            matrix = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=matrix)

            # 根据格式保存
            format_upper = format.upper()
            if format_upper == "JPG" or format_upper == "JPEG":
                # JPG不支持透明通道，需要先转换为RGB
                if pix.n == 4:
                    img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples[: pix.width * pix.height * 3])
                else:
                    img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
            else:
                # PNG支持RGBA
                img = Image.frombytes("RGBA" if pix.n == 4 else "RGB", (pix.width, pix.height), pix.samples)

            img.save(output_path, format=format_upper if format_upper != "JPG" else "JPEG")
            logger.info("保存页面 %d 为图像成功: %s", page_num, output_path)
            return True

        except Exception as e:
            logger.error("保存页面 %d 失败: %s", page_num, str(e))
            return False

    def close(self) -> None:
        """关闭PDF文档，释放资源"""
        if self._document is not None:
            self._document.close()
            self._document = None
            self._page_count = None
            logger.debug("PDF文档已关闭")

    def __enter__(self) -> "PDFProcessor":
        """上下文管理器入口"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """上下文管理器退出，自动关闭文档"""
        self.close()

    def __del__(self) -> None:
        """析构函数，确保资源释放"""
        self.close()
