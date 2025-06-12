def replace_quotes(text: str) -> str:
    """将双引号替换为单引号"""
    return text.replace('"', "'")

def format_comma_str(input_str: str) -> str:
    """格式化逗号分隔字符串"""
    return ','.join([f"'{item.strip()}'" for item in input_str.split(',')])

def format_space_to_comma(input_str: str) -> str:
    """空格替换为逗号"""
    return ','.join(input_str.split())

