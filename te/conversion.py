# 主程序入口
import streamlit as st
from ui import ui_components
from core import text_processor, video_merger
from utils import config_manager
import sys
import os

# 初始化应用
def main():
    # 应用配置
    config_manager.AppConfig.setup_config()
    # 检查依赖
    MOVIEPY_AVAILABLE = video_merger.check_moviepy_availability()
    # 初始化UI
    ui_components.initialize_ui(MOVIEPY_AVAILABLE)

    # 根据选择执行功能
    func_choice = ui_components.function_selector(MOVIEPY_AVAILABLE)
    if func_choice == "合并多个视频" and MOVIEPY_AVAILABLE:
        video_merger.handle_video_merge()
    else:
        text_processor.handle_text_processing(func_choice)



if __name__ == "__main__":
    main()