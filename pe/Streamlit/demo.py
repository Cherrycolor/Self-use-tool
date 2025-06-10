import streamlit as st
import os
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.compositing.CompositeVideoClip import concatenate_videoclips
from tempfile import NamedTemporaryFile

# 设置页面配置（增加视频上传大小限制为2GB）
st.set_page_config(
    page_title="g文本格式处理工具",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS样式（新增视频预览区样式）
st.markdown("""
<style>
/* 全局样式 */
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

# 创建配置文件目录
if not os.path.exists(".streamlit"):
    os.makedirs(".streamlit")

# 写入配置文件（设置2GB上传限制）
config_content = "[server]\nmaxUploadSize = 2000"
with open(".streamlit/config.toml", "w") as f:
    f.write(config_content)


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


# 新增视频合并函数
def merge_videos(uploaded_files):
    """合并多个视频文件"""
    clips = []
    temp_files = []

    # 保存上传文件到临时目录
    for uploaded_file in uploaded_files:
        with NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
            temp_file.write(uploaded_file.read())
            temp_files.append(temp_file.name)

    # 逐个加载视频
    for temp_file in temp_files:
        clip = VideoFileClip(temp_file)
        clips.append(clip)

    # 合并视频
    final_clip = concatenate_videoclips(clips)

    # 生成输出文件
    output_path = "merged_video.mp4"
    final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")

    # 清理临时文件
    for clip in clips:
        clip.close()
    for temp_file in temp_files:
        os.unlink(temp_file)

    return output_path


# 界面布局
st.title("📝 g文本格式处理工具")

# 功能选择 - 新增视频合并选项
func_choice = st.radio(
    "选择功能",
    ["替换双引号为单引号", "格式化逗号分隔字符串", "空格替换为逗号", "合并多个视频"],
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
    else:  # 视频合并示例
        st.markdown("""
        **使用说明:**
        1. 上传多个MP4视频文件（最多可上传2GB大小的文件）
        2. 点击"合并视频"按钮
        3. 合并完成后可预览并下载结果视频
        """)

# 视频合并功能实现
if func_choice == "合并多个视频":
    st.subheader("视频合并工具")

    # 多文件上传（支持最大2GB）
    uploaded_files = st.file_uploader(
        "选择多个视频文件（MP4格式）",
        type=["mp4"],
        accept_multiple_files=True,
        help="支持同时选择多个文件，总大小不超过2GB"
    )

    if uploaded_files:
        total_size = sum(file.size for file in uploaded_files)
        st.info(f"已选择 {len(uploaded_files)} 个文件，总大小: {total_size / 1024 / 1024:.2f} MB")

        # 显示预览
        cols = st.columns(min(3, len(uploaded_files)))
        for i, file in enumerate(uploaded_files):
            with cols[i % 3]:
                st.video(file, format="video/mp4")  #
                st.caption(file.name)

    # 合并按钮
    if st.button("🚀 合并视频", disabled=len(uploaded_files) < 2):
        with st.spinner("视频合并中，请稍候..."):
            try:
                output_path = merge_videos(uploaded_files)

                # 显示合并结果
                st.success("视频合并完成！")
                st.subheader("合并结果预览")
                st.video(output_path, format="video/mp4")

                # 提供下载
                with open(output_path, "rb") as f:
                    st.download_button(
                        label="📥 下载合并后的视频",
                        data=f,
                        file_name="merged_video.mp4",
                        mime="video/mp4"
                    )

                # 清理生成的文件
                os.unlink(output_path)

            except Exception as e:
                st.error(f"视频合并失败: {str(e)}")

# 原有文本处理功能
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
                else:
                    output = format_blank(input_text)

                # 显示结果
                st.subheader("处理结果")
                st.code(output, language='plaintext')

                # 下载功能
                st.download_button(
                    label="📥 下载结果",
                    data=output,
                    file_name='result.txt',
                    mime='text/plain'
                )
            except Exception as e:
                st.error(f"处理出错: {str(e)}")
        else:
            st.warning("请输入有效内容！")

# 配置提示
st.sidebar.info("""
**配置说明**  
已启用2GB大文件上传支持  
配置文件路径: `.streamlit/config.toml`
""")