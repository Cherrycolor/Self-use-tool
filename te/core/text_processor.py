import streamlit as st

def replace_quotes(text: str) -> str:
    """将双引号替换为单引号"""
    return text.replace('"', "'")

def format_comma_str(input_str: str) -> str:
    """格式化逗号分隔字符串"""
    return ','.join([f"'{item.strip()}'" for item in input_str.split(',')])

def format_space_to_comma(input_str: str) -> str:
    """空格替换为逗号"""
    return ','.join(input_str.split())

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
                "替换双引号为单引号": replace_quotes,
                "格式化逗号分隔字符串": format_comma_str,
                "空格替换为逗号": format_space_to_comma
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

