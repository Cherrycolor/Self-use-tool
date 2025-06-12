from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.compositing.CompositeVideoClip import concatenate_videoclips
from utils.file_utils import temporary_files  # 复用工具函数 ；以谁作为主程序开始运行，谁就是顶层目录，所以这样导入没问题
from contextlib import contextmanager

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