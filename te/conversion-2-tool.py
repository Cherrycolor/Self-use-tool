import streamlit as st
import altair as alt  # 导入Altair库

# 设置页面配置
st.set_page_config(page_title="g文本格式处理工具", layout="wide")

# 自定义CSS样式
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
</style>
""", unsafe_allow_html=True)

# 启用Altair 5.5.0的HTML渲染器
alt.renderers.enable('html')


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
st.title("g文本格式处理工具")

# 功能选择
func_choice = st.radio("选择功能", ["替换双引号为单引号", "格式化逗号分隔字符串", "空格替换为逗号"])

# 动态显示使用示例
with st.expander("点击查看使用示例", expanded=True):
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
    else:
        st.markdown("""
        **示例输入输出:**
        - '2079 2077 2074' → '2079,2077,2074'
        """)

# 输入方式
input_type = st.radio("输入方式", ["直接输入", "上传文件"])

# 处理输入内容
input_text = ""
if input_type == "直接输入":
    if func_choice == "替换双引号为单引号":
        input_text = st.text_area("输入文本", height=200)
    elif func_choice == "格式化逗号分隔字符串":
        input_text = st.text_input("输入逗号分隔的字符串")
    else:
        input_text = st.text_input("请输入要查询的 ID(用空格分隔)")
else:
    uploaded_file = st.file_uploader("选择文件", type=["txt"])
    if uploaded_file:
        bytes_data = uploaded_file.getvalue()
        input_text = bytes_data.decode("utf-8")

# 处理按钮
if st.button("执行处理"):
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
                label="下载结果",
                data=output,
                file_name='result.txt',
                mime='text/plain'
            )

            # 添加Altair可视化示例（展示字符统计）
            char_count = len(output.replace(" ", "").replace(",", ""))
            word_count = len(output.split())

            data = alt.Data(values=[
                {'category': '字符数', 'value': char_count},
                {'category': '单词数', 'value': word_count}
            ])

            chart = alt.Chart(data).mark_bar().encode(
                x='category:N',
                y='value:Q',
                color=alt.Color('category:N', legend=None)
            ).properties(
                title='文本统计',
                width=300
            )

            st.altair_chart(chart)  # 使用Altair 5.5.0 API渲染图表

        except Exception as e:
            st.error(f"处理出错: {str(e)}")
    else:
        st.warning("请输入有效内容!")