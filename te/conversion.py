# 主程序入口
import streamlit as st
from ui import ui_components
from core import text_processor, video_merger
from utils import file_utils, config_manager
import sys
import os

# 初始化应用
def main():
    # 应用配置
    config_manager.AppConfig.setup_config()

    # 初始化UI
    st.set_page_config(
        page_title="📝 文本格式处理工具",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    ui_components.apply_custom_styles()

    # 检查依赖
    MOVIEPY_AVAILABLE = video_merger.check_moviepy_availability()

    # 显示侧边栏信息
    ui_components.show_sidebar_info(MOVIEPY_AVAILABLE)

    # 主界面
    st.title("📝 文本格式处理工具")

    # 功能路由
    func_choice = ui_components.function_selector(MOVIEPY_AVAILABLE)
    ui_components.show_function_examples(func_choice)

    # 根据选择执行功能
    if func_choice == "合并多个视频" and MOVIEPY_AVAILABLE:
        handle_video_merge()
    else:
        handle_text_processing(func_choice)


# 视频处理路由
def handle_video_merge():
    st.subheader("🎬 视频合并工具")
    uploaded_files = st.file_uploader(
        "选择多个视频文件",
        type=["mp4", "mov", "avi"],
        accept_multiple_files=True,
        help="支持同时选择多个文件，总大小不超过2GB"
    )

    if uploaded_files:
        total_size = sum(file.size for file in uploaded_files)
        st.info(f"已选择 {len(uploaded_files)} 个文件，总大小: {total_size / 1024 / 1024:.2f} MB")

    if st.button("🚀 合并视频", type="primary", disabled=len(uploaded_files) < 2):
        with st.spinner("视频合并中，请稍候..."):
            try:
                output_path = video_merger.merge_videos(uploaded_files)
                st.success("✅ 视频合并完成！")

                # 提供下载
                with open(output_path, "rb") as f:
                    st.download_button(
                        label="📥 下载合并后的视频",
                        data=f,
                        file_name="merged_video.mp4",
                        mime="video/mp4"
                    )

                # 清理生成的文件
                if os.path.exists(output_path):
                    os.unlink(output_path)
            except Exception as e:
                st.error(f"❌ 视频合并失败: {str(e)}")
                st.exception(e)


# 文本处理路由
def handle_text_processing(func_choice):
    # 输入方式选择
    input_type = st.radio(
        "📥 输入方式",
        ["直接输入", "上传文件"],
        horizontal=True
    )

    # 获取输入内容
    input_text = ""
    if input_type == "直接输入":
        if func_choice == "替换双引号为单引号":
            input_text = st.text_area("输入文本", height=200)
        elif func_choice == "格式化逗号分隔字符串":
            input_text = st.text_input("输入逗号分隔的字符串")
        else:
            input_text = st.text_input("请输入要查询的 ID（用空格分隔）")
    else:
        uploaded_file = st.file_uploader("选择文件", type=["txt"])
        if uploaded_file:
            input_text = uploaded_file.getvalue().decode("utf-8")

    # 处理并显示结果
    if st.button("🚀 执行处理"):
        if not input_text.strip():
            st.warning("⚠️ 请输入有效内容！")
            return

        try:
            # 策略模式调用处理函数
            processor_map = {
                "替换双引号为单引号": text_processor.replace_quotes,
                "格式化逗号分隔字符串": text_processor.format_comma_str,
                "空格替换为逗号": text_processor.format_space_to_comma
            }
            output = processor_map[func_choice](input_text)

            # 显示结果
            st.subheader("📝 处理结果")
            st.code(output, language='plaintext')

            # 下载功能
            st.download_button(
                label="📥 下载结果",
                data=output,
                file_name='result.txt',
                mime='text/plain'
            )
        except Exception as e:
            st.error(f"❌ 处理出错: {str(e)}")


if __name__ == "__main__":
    main()