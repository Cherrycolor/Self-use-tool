import streamlit as st

# 设置页面配置
st.set_page_config(page_title="📝 文本格式处理工具", layout="wide")

# 自定义CSS样式
st.markdown("""
<style>
    .stButton>button {
        background-color: #e95678; /* 按钮背景色 */
        color: white;
        border: none;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .stTextArea textarea, .stTextInput input, .stFileUploader [type=file] {
        border: 1px solid #dfe1e5;
        border-radius: 8px;
    }
    .stExpanderHeader {
        background-color: #f0f2f5;
        padding: 10px;
        border-radius: 8px 8px 0 0;
    }
</style>
""", unsafe_allow_html=True)


# 保留原核心处理函数
def replace_quotes(text):
    """将双引号替换为单引号"""
    return text.replace('"', "'")


def format_string(input_str):
    """格式化逗号分隔字符串"""
    return ','.join([f"'{item.strip()}'" for item in input_str.split(',')])


def format_blank(input_str):
    """空格替换为逗号"""
    return ','.join(input_str.split())


# 界面布局
st.title("📝 文本格式处理工具 📄")

# 功能选择
func_choice = st.radio("选择功能 🛠️", ["替换双引号为单引号", "格式化逗号分隔字符串", "空格替换为逗号"])

# 动态显示使用示例
with st.expander("🖱️ 点击查看使用示例 📝", expanded=True):
    if func_choice == "替换双引号为单引号":
        st.markdown("""
        **示例输入输出：**  
        `"Hello World"` ➔ `'Hello World'`  
        `"Data" -> "Science"` ➔ `'Data' -> 'Science'`
        """)
    elif func_choice == "格式化逗号分隔字符串":
        st.markdown("""
        **示例输入输出：**  
        `JM81558,SQ60230,JM20534` ➔ `'JM81558','SQ60230','JM20534'`  
        `2079, 2077, 2074` ➔ `'2079','2077','2074'`
        """)
    else:
        st.markdown("""
        **示例输入输出：**
        `2079 2077 2074` ➔ `2079,2077,2074`
        """)

# 输入方式
input_type = st.radio("输入方式 📋", ["直接输入", "上传文件"])

# 处理输入内容
input_text = ""
if input_type == "直接输入":
    if func_choice == "替换双引号为单引号":
        input_text = st.text_area("输入文本 📝", height=200)
    elif func_choice == "格式化逗号分隔字符串":
        input_text = st.text_input("输入逗号分隔的字符串 📑")
    else:
        input_text = st.text_input("请输入要查询的ID（用空格分隔） 🖇️")
else:
    uploaded_file = st.file_uploader("选择文件 📁", type=["txt"])
    if uploaded_file:
        bytes_data = uploaded_file.getvalue()
        input_text = bytes_data.decode("utf-8")

# 处理按钮
if st.button("✨ 执行处理 ✨"):
    if input_text.strip():
        try:
            if func_choice == "替换双引号为单引号":
                output = replace_quotes(input_text)
            elif func_choice == "格式化逗号分隔字符串":
                output = format_string(input_text)
            else:
                output = format_blank(input_text)

            # 显示结果
            st.subheader("处理结果 📊")
            st.code(output, language='plaintext')

            # 下载功能
            st.download_button(
                label="⬇️ 下载结果 ⬇️",
                data=output,
                file_name='result.txt',
                mime='text/plain'
            )
        except Exception as e:
            st.error(f"处理出错: {str(e)}")
    else:
        st.warning("请输入有效内容！")
