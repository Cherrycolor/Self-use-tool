from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.compositing.CompositeVideoClip import concatenate_videoclips
from utils.file_utils import temporary_files  # 复用工具函数 ；以谁作为主程序开始运行，谁就是顶层目录，所以这样导入没问题
from contextlib import contextmanager
import streamlit as st
import os

# core/video_merger.py - 视频处理核心逻辑
def check_moviepy_availability():
    """检查MoviePy是否可用"""
    try:
        from moviepy.video.io.VideoFileClip import VideoFileClip
        from moviepy.video.compositing.CompositeVideoClip import concatenate_videoclips

        return True
    except ImportError:
        return False

@contextmanager
def video_clip_manager(file_paths):
    """上下文管理器用于安全处理视频剪辑"""
    clips = []
    try:
        for path in file_paths:
            clip = VideoFileClip(path)
            clips.append(clip)
        yield clips
    finally:
        for clip in clips:
            try:
                clip.close()
            except Exception:
                pass

def merge_videos(uploaded_files) -> str:
    """合并多个视频文件"""
    with temporary_files(uploaded_files) as temp_paths:
        with video_clip_manager(temp_paths) as clips:
            final_clip = concatenate_videoclips(clips)
            output_path = "merged_video.mp4"
            final_clip.write_videofile(
                output_path,
                codec="libx264",
                audio_codec="aac",
                threads=4  # 多线程加速处理
            )
            return output_path

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
                output_path = merge_videos(uploaded_files)
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