"""文本处理工具"""

import re
from typing import List, Tuple


def split_text_by_size(text: str, chunk_size: int = 1000, overlap: int = 100) -> List[str]:
    """按大小分割文本"""
    chunks = []
    start = 0
    text_length = len(text)
    
    while start < text_length:
        end = min(start + chunk_size, text_length)
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap
    
    return chunks


def split_text_by_paragraph(text: str) -> List[str]:
    """按段落分割文本"""
    paragraphs = re.split(r'\n\s*\n', text)
    return [p.strip() for p in paragraphs if p.strip()]


def split_text_by_sentence(text: str) -> List[str]:
    """按句子分割文本"""
    sentences = re.split(r'[。！？.!?]\s*', text)
    return [s.strip() for s in sentences if s.strip()]


def clean_text(text: str) -> str:
    """清理文本"""
    # 移除多余的空白字符
    text = re.sub(r'\s+', ' ', text)
    # 移除首尾空白
    text = text.strip()
    return text


def truncate_text(text: str, max_length: int) -> str:
    """截断文本"""
    if len(text) <= max_length:
        return text
    return text[:max_length] + '...'


def count_tokens(text: str) -> int:
    """估算token数量"""
    # 简单估算，实际应使用具体的tokenizer
    return len(text.split())
