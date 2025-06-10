import argparse
import sys

"""
数据格式转换工具 v1.1

功能：
1. 替换双引号为单引号
2. 格式化逗号分隔字符串

效果示例：
1. "Hello World" 转换为 'Hello World'
2. JM81558,SQ60230,JM20534   ->   'JM81558','SQ60230','JM20534'
"""

def replace_quotes(text):
    """将文本中的所有双引号替换为单引号"""
    return text.replace('"', "'")

def format_string(input_str):
    """核心处理函数：将逗号分隔的字符串转换为单引号包裹的格式"""
    return ','.join([f"'{item.strip()}'" for item in input_str.split(',')])

def interactive_mode():
    """交互式模式处理函数"""
    print("请选择功能：")
    print("1. 替换双引号为单引号")
    print("2. 格式化逗号分隔的字符串")
    func_choice = input("请输入选项数字 (1/2): ")
    if func_choice not in ['1', '2']:
        print("无效选择")
        sys.exit(1)

    print("请选择输入方式：")
    print("1. 直接输入")
    print("2. 从文件读取")
    input_choice = input("请输入选项数字 (1/2): ")
    if input_choice not in ['1', '2']:
        print("无效输入方式")
        sys.exit(1)

    input_text = ''
    if func_choice == '1':
        # 处理替换双引号功能的输入
        if input_choice == '1':
            print("\n请输入要处理的文本（输入空行后按回车确认）：")
            lines = []
            while True:
                line = input()
                if line == "":
                    break
                lines.append(line)
            input_text = '\n'.join(lines)
        else:
            filepath = input("\n请输入文件路径: ")
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    input_text = f.read()
            except FileNotFoundError:
                print(f"错误：文件 {filepath} 不存在")
                sys.exit(1)
            except Exception as e:
                print(f"读取文件出错: {str(e)}")
                sys.exit(1)
    else:
        # 处理格式化功能的输入
        if input_choice == '1':
            print("\n请输入逗号分隔的字符串：")
            input_text = input().strip()
        else:
            filepath = input("\n请输入文件路径: ")
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    input_text = f.read().strip()
            except FileNotFoundError:
                print(f"错误：文件 {filepath} 不存在")
                sys.exit(1)
            except Exception as e:
                print(f"读取文件出错: {str(e)}")
                sys.exit(1)

    if not input_text.strip():
        print("输入内容不能为空！")
        sys.exit(1)

    # 执行相应处理
    if func_choice == '1':
        output_text = replace_quotes(input_text)
    else:
        output_text = format_string(input_text)

    # 显示结果
    print("\n处理结果：")
    print("-" * 40)
    print(output_text)
    print("-" * 40)

    # 保存文件选项
    save_choice = input("\n是否保存到文件？ (y/n): ").lower()
    if save_choice == 'y':
        save_path = input("请输入保存路径: ")
        try:
            with open(save_path, 'w', encoding='utf-8') as f:
                f.write(output_text)
            print(f"文件已保存至 {save_path}")
        except Exception as e:
            print(f"保存文件失败: {str(e)}")

def main():
    """主函数"""
    if len(sys.argv) == 1:
        interactive_mode()
    else:
        parser = argparse.ArgumentParser(description='数据格式转换工具 v1.0')
        subparsers = parser.add_subparsers(dest='command', help='子命令')

        # Replace 命令
        replace_parser = subparsers.add_parser('replace', help='将双引号替换为单引号')
        replace_parser.add_argument('-i', '--input', help='直接输入文本')
        replace_parser.add_argument('-f', '--file', help='输入文件路径')
        replace_parser.add_argument('-o', '--output', help='输出文件路径')

        # Format 命令
        format_parser = subparsers.add_parser('format', help='格式化逗号分隔的字符串')
        format_parser.add_argument('-i', '--input', help='直接输入字符串')
        format_parser.add_argument('-f', '--file', help='输入文件路径')
        format_parser.add_argument('-o', '--output', help='输出文件路径')

        args = parser.parse_args()

        if not hasattr(args, 'command'):
            print("错误：请指定一个有效的子命令（replace 或 format）")
            sys.exit(1)

        # 处理输入内容
        input_text = ''
        if args.command in ['replace', 'format']:
            if args.input:
                input_text = args.input
            elif args.file:
                try:
                    with open(args.file, 'r', encoding='utf-8') as f:
                        input_text = f.read()
                        if args.command == 'format':
                            input_text = input_text.strip()
                except FileNotFoundError:
                    print(f"错误：文件 {args.file} 未找到")
                    sys.exit(1)
                except Exception as e:
                    print(f"读取文件出错: {str(e)}")
                    sys.exit(1)
            else:
                print("错误：需要指定输入源（-i 或 -f）")
                sys.exit(1)

        # 处理并生成结果
        if args.command == 'replace':
            output_text = replace_quotes(input_text)
        elif args.command == 'format':
            output_text = format_string(input_text)
        else:
            print("错误：未知命令")
            sys.exit(1)

        # 输出结果
        print("\n处理结果：")
        print(output_text)

        # 保存到文件
        if args.output:
            try:
                with open(args.output, 'w', encoding='utf-8') as f:
                    f.write(output_text)
                print(f"文件已保存至 {args.output}")
            except Exception as e:
                print(f"保存文件失败: {str(e)}")

if __name__ == "__main__":
    main()