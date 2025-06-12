# 文件工具
import os
import tempfile
from contextlib import contextmanager

@contextmanager
def temporary_files(files):
    """上下文管理临时文件"""
    temp_paths = []
    try:
        for file in files:
            suffix = os.path.splitext(file.name)[1]
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
                temp_file.write(file.getvalue())
                temp_paths.append(temp_file.name)
        yield temp_paths
    finally:
        for path in temp_paths:
            if os.path.exists(path):
                try:
                    os.unlink(path)
                except Exception:
                    pass