# 配置管理
import os

class AppConfig:
    CONFIG_DIR = ".streamlit"
    CONFIG_FILE = "config.toml"

    @classmethod
    def setup_config(cls):
        """创建配置文件目录"""
        if not os.path.exists(cls.CONFIG_DIR):
            os.makedirs(cls.CONFIG_DIR)

        config_path = os.path.join(cls.CONFIG_DIR, cls.CONFIG_FILE)
        if not os.path.exists(config_path):
            with open(config_path, "w") as f:
                f.write("[server]\nmaxUploadSize = 2000")  # 设置2GB上传限制