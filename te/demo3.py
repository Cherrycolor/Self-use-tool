import streamlit as st
import os
import tempfile
import sys
from contextlib import contextmanager
import subprocess

# 设置页面配置
st.set_page_config(
    page_title="📝 文本格式处理工具",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS样式（新增视频预览区样式）
st.markdown("""
<style>
.stButton>button {
    background-color: #e95678;
    color: white;
    border: none;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.stTextArea textarea, .stTextInput input, .stFileUploader[type=file] {
    border: 1px solid #dfe1e5;
    border-radius: 8px;
}

.stExpanderHeader {
    background-color: #f0f2f5;
    padding: 10px;
    border-radius: 8px 8px 0 0;
}

/* 新增视频预览区样式 */
.video-preview {
    max-width: 100%;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    margin-bottom: 16px;
}
</style>
""", unsafe_allow_html=True)

# 创建配置文件目录（用于大文件上传）
if not os.path.exists(".streamlit"):
    os.makedirs(".streamlit")
config_path = os.path.join(".streamlit", "config.toml")
if not os.path.exists(config_path):
    with open(config_path, "w") as f:
        f.write("[server]\nmaxUploadSize = 2000")  # 设置2GB上传限制

# 视频处理库导入（带兼容性检查）
try:
    from moviepy.video.io.VideoFileClip import VideoFileClip
    from moviepy.video.compositing.CompositeVideoClip import concatenate_videoclips

    MOVIEPY_AVAILABLE = True
except (ImportError, ModuleNotFoundError) as e:
    st.warning(f"视频处理功能不可用: {str(e)}")
    MOVIEPY_AVAILABLE = False


# 核心文本处理函数
def replace_quotes(text):
    """将双引号替换为单引号"""
    return text.replace('"', "'")


def format_string(input_str):
    """格式化逗号分隔字符串"""
    return ','.join([f"'{item.strip()}'" for item in input_str.split(',')])


def format_blank(input_str):
    """空格替换为逗号"""
    return ','.join(input_str.split())


# 视频合并功能（带兼容性检查）
def merge_videos(uploaded_files):
    """合并多个视频文件"""
    if not MOVIEPY_AVAILABLE:
        raise RuntimeError("视频处理库不可用")

    # 临时文件管理器
    @contextmanager
    def temporary_files(files):
        temp_paths = []
        try:
            for file in files:
                # 创建临时文件
                suffix = os.path.splitext(file.name)[1]  # 保留原始扩展名
                with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
                    temp_file.write(file.getvalue())
                    temp_paths.append(temp_file.name)
            yield temp_paths
        finally:
            for path in temp_paths:
                if os.path.exists(path):
                    os.unlink(path)

    # 合并处理
    with temporary_files(uploaded_files) as temp_paths:
        clips = []
        try:
            # 加载所有视频剪辑
            for path in temp_paths:
                clip = VideoFileClip(path)
                clips.append(clip)

            # 合并视频
            final_clip = concatenate_videoclips(clips)

            # 生成输出文件
            output_path = "merged_video.mp4"
            final_clip.write_videofile(
                output_path,
                codec="libx264",
                audio_codec="aac",
                threads=4  # 使用多线程加速处理
            )

            return output_path
        finally:
            # 关闭所有剪辑释放资源
            for clip in clips:
                try:
                    clip.close()
                except:
                    pass


# 界面布局
st.title("📝 文本格式处理工具")

# 功能选择 - 添加视频合并选项
func_choices = ["替换双引号为单引号", "格式化逗号分隔字符串", "空格替换为逗号"]
if MOVIEPY_AVAILABLE:
    func_choices.append("合并多个视频")

func_choice = st.radio(
    "选择功能",
    func_choices,
    horizontal=True
)

# 动态显示使用示例
with st.expander("📌 点击查看使用示例", expanded=True):
    if func_choice == "替换双引号为单引号":
        st.markdown("""
        **示例输入输出:**
        - "Hello World" → 'Hello World'
        - "Data"->"Science" → 'Data'->'Science'
        """)
    elif func_choice == "格式化逗号分隔字符串":
        st.markdown("""
        **示例输入输出:**
        - 'JM81558, SQ60230, JM20534' → 'JM81558','SQ60230','JM20534'
        - '2079, 2077, 2074' → '2079','2077','2074'
        """)
    elif func_choice == "空格替换为逗号":
        st.markdown("""
        **示例输入输出:**
        - '2079 2077 2074' → '2079,2077,2074'
        """)
    elif func_choice == "合并多个视频":
        st.markdown("""
        **使用说明:**
        1. 上传多个视频文件（支持MP4、MOV等格式）
        2. 点击"合并视频"按钮
        3. 合并完成后可下载结果视频
        *注意：视频总大小不超过2GB*
        """)

# 视频合并功能实现
if func_choice == "合并多个视频" and MOVIEPY_AVAILABLE:
    st.subheader("🎬 视频合并工具")

    # 多文件上传（支持最大2GB）
    uploaded_files = st.file_uploader(
        "选择多个视频文件",
        type=["mp4", "mov", "avi"],
        accept_multiple_files=True,
        help="支持同时选择多个文件，总大小不超过2GB"
    )

    if uploaded_files:
        total_size = sum(file.size for file in uploaded_files)
        st.info(f"已选择 {len(uploaded_files)} 个文件，总大小: {total_size / 1024 / 1024:.2f} MB")

    # 合并按钮
    if st.button("🚀 合并视频", type="primary", disabled=len(uploaded_files) < 2):
        with st.spinner("视频合并中，请稍候..."):
            try:
                output_path = merge_videos(uploaded_files)

                # 显示合并结果
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
                # 显示详细错误信息
                st.exception(e)

# 文本处理功能
else:
    # 输入方式
    input_type = st.radio(
        "📥 输入方式",
        ["直接输入", "上传文件"],
        horizontal=True
    )

    # 处理输入内容
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

    # 处理按钮
    if st.button("🚀 执行处理"):
        if input_text.strip():
            try:
                if func_choice == "替换双引号为单引号":
                    output = replace_quotes(input_text)
                elif func_choice == "格式化逗号分隔字符串":
                    output = format_string(input_text)
                elif func_choice == "空格替换为逗号":
                    output = format_blank(input_text)

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
        else:
            st.warning("⚠️ 请输入有效内容！")

# 环境信息
st.sidebar.info(f"""
**运行环境信息**  
Python版本: {sys.version.split()[0]}  
Streamlit版本: {st.__version__}  
视频处理功能: {'✅ 可用' if MOVIEPY_AVAILABLE else '❌ 不可用'}  
最大上传限制: 2GB  
""")

# 安装指引
if not MOVIEPY_AVAILABLE:
    st.sidebar.warning("""
    **缺少视频处理依赖**  
    需要安装MoviePy库才能使用视频合并功能：
    ```bash
    pip install moviepy
    ```
    """)