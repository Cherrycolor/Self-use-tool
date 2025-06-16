import streamlit as st

def initialize_ui(MOVIEPY_AVAILABLE):
    st.set_page_config(
        page_title="📝 文本格式处理工具",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    apply_custom_styles()

    st.title("📝 文本格式处理工具")  # 主界面
    show_sidebar_info(MOVIEPY_AVAILABLE) # 显示侧边栏信息

    func_choice = function_selector(MOVIEPY_AVAILABLE) # 功能路由
    show_function_examples(func_choice) # 显示侧边栏信息

def apply_custom_styles():
    """应用自定义CSS样式"""
    st.markdown("""
    <style>
    /* 按钮样式 */
    .stButton>button {
        background-color: #e95678;
        color: white;
        border: none;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }

    /* 输入框样式 */
    .stTextArea textarea, .stTextInput input, .stFileUploader[type=file] {
        border: 1px solid #dfe1e5;
        border-radius: 8px;
    }

    /* 侧边栏样式 */
    .stExpanderHeader {
        background-color: #f0f2f5;
        padding: 10px;
        border-radius: 8px 8px 0 0;
    }

    /* 视频预览区样式 */
    .video-preview {
        max-width: 100%;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        margin-bottom: 16px;
    }
    </style>
    """, unsafe_allow_html=True)

def show_function_examples(func_choice: str):
    """动态显示功能示例"""
    examples = {
        "替换双引号为单引号": """
        **示例输入输出:**
        - "Hello World" → 'Hello World'
        - "Data"->"Science" → 'Data'->'Science'
        """,

        "格式化逗号分隔字符串": """
        **示例输入输出:**
        - 'JM81558, SQ60230, JM20534' → 'JM81558','SQ60230','JM20534'
        - '2079, 2077, 2074' → '2079','2077','2074'
        """,

        "空格替换为逗号":"""
        **示例输入输出:**
        - '2079 2077 2074' → '2079,2077,2074'
        """,

        "合并多个视频":"""
        **使用说明:**
        1. 上传多个视频文件（支持MP4、MOV等格式）
        2. 点击"合并视频"按钮
        3. 合并完成后可下载结果视频
        *注意：视频总大小不超过2GB*
        """
    }
    with st.expander("📌 点击查看使用示例", expanded=True):
        st.markdown(examples.get(func_choice, "暂无示例"))


def function_selector(moviepy_available: bool) -> str:
    """功能选择器"""
    func_choices = ["替换双引号为单引号", "格式化逗号分隔字符串", "空格替换为逗号"]
    if moviepy_available:
        func_choices.append("合并多个视频")

    return st.radio(
        "选择功能",
        func_choices,
        horizontal=True
    )


def show_sidebar_info(moviepy_available: bool):
    """显示侧边栏环境信息"""
    import sys
    env_info = f"""
    **运行环境信息**  
    Python版本: {sys.version.split()[0]}  
    Streamlit版本: {st.__version__}  
    视频处理功能: {'✅ 可用' if moviepy_available else '❌ 不可用'}  
    最大上传限制: 2GB
    """

    st.sidebar.info(env_info)

    if not moviepy_available:
        st.sidebar.warning("""
        **缺少视频处理依赖**
        需要安装MoviePy库才能使用视频合并功能：
        ```bash
        pip install moviepy
        ```
        """)