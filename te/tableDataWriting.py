import os
import random
import pandas as pd
from openpyxl import load_workbook
from faker import Faker
import datetime
from openpyxl.utils import get_column_letter
from openpyxl.styles import Alignment
import numpy as np

# 初始化Faker生成中文数据
fake = Faker('zh_CN')

# 硬编码所有下拉选项数据（从模板解析结果中提取）
BIRTHPLACE_OPTIONS = [
    "北京市", "天津市", "石家庄市", "太原市", "呼和浩特市", "沈阳市", "长春市", "哈尔滨市", "上海市", "南京市",
    "杭州市", "合肥市", "福州市", "南昌市", "济南市", "郑州市", "武汉市", "长沙市", "广州市", "南宁市",
    "海口市", "重庆市", "成都市", "贵阳市", "昆明市", "西安市", "兰州市", "西宁市", "银川市", "乌鲁木齐市"
]

INDUSTRY_OPTIONS = [
    ("汽车", "汽车销售"), ("汽车", "汽车租赁"), ("汽车", "汽车服务"),
    ("房地产", "房产销售"), ("房地产", "房产租赁"), ("房地产", "房产服务"),
    ("食品酒饮", "休闲食品"), ("食品酒饮", "粮油调味"), ("食品酒饮", "生鲜蔬菜"),
    ("食品酒饮", "烟酒饮料"), ("个护清洁", "个人护理"), ("个护清洁", "家庭护理"),
    ("电子产品", "手机"), ("电子产品", "电脑办公"), ("电子产品", "数码相机"),
    ("电子产品", "影音娱乐"), ("电子产品", "智能设备"), ("教育培训", "教育培训"),
    ("钟表珠宝", "钟表珠宝"), ("服饰鞋包", "男装女装"), ("服饰鞋包", "男鞋女鞋"),
    ("服饰鞋包", "箱包"), ("服饰鞋包", "服饰配件"), ("母婴亲子", "母婴用品"),
    ("母婴亲子", "母婴服务"), ("互联网", "基础服务"), ("互联网", "商务应用"),
    ("互联网", "交流娱乐"), ("互联网", "媒体"), ("互联网", "共享经济")
]

BUSINESS_OPTIONS = [
    ("零售", "女装"), ("零售", "男装"), ("零售", "男女装集合"), ("零售", "其他服饰"),
    ("零售", "鞋品箱包"), ("零售", "烟酒"), ("零售", "茶叶"), ("零售", "水果"),
    ("零售", "零食"), ("零售", "饮品"), ("零售", "米面粮油"), ("零售", "其他食品"),
    ("零售", "数码电子"), ("零售", "家电"), ("零售", "黄金珠宝"), ("零售", "钟表"),
    ("零售", "配饰"), ("零售", "杂品"), ("零售", "大型连锁超市"), ("零售", "便利店"),
    ("零售", "小型超市"), ("零售", "生鲜超市"), ("零售", "花店"), ("零售", "免税店"),
    ("零售", "OUTLETS"), ("零售", "家居家用"), ("零售", "商用设备"), ("零售", "农用设备"),
    ("零售", "工业设备"), ("零售", "五金建材"), ("零售", "办公耗材"), ("零售", "运动户外"),
    ("零售", "自行车"), ("零售", "电瓶车"), ("零售", "其他出行工具"), ("零售", "个护美妆"),
    ("零售", "药品器械"), ("零售", "保健品"), ("餐饮", "地方菜系"), ("餐饮", "异国餐饮"),
    ("餐饮", "自助餐"), ("餐饮", "烧烤"), ("餐饮", "锅类"), ("餐饮", "小吃快餐"),
    ("餐饮", "咖啡"), ("餐饮", "茶饮"), ("餐饮", "其他饮品"), ("餐饮", "烘焙"),
    ("餐饮", "甜品"), ("餐饮", "美食广场"), ("餐饮", "主题餐厅"), ("餐饮", "酒吧")
]


def generate_random_brand_data(num_records=100):
    """生成随机品牌数据"""
    brands = []

    for _ in range(num_records):
        # 随机选择行业和业态
        primary_industry, secondary_industry = random.choice(INDUSTRY_OPTIONS)
        primary_business, secondary_business = random.choice(BUSINESS_OPTIONS)

        # 随机生成成立时间 (1949-2023年)
        founding_year = random.randint(1949, 2023)
        founding_date = f"{founding_year}"

        brand = {
            "*品牌名称": f"{fake.company_prefix()}{fake.word()}",
            "一级所属行业": primary_industry,
            "二级所属行业": secondary_industry,
            "*品牌类型": random.choice(["买家品牌", "供应商品牌","服务商品牌","其他品牌"]),
            "成立时间": founding_date,
            "发源地": random.choice(BIRTHPLACE_OPTIONS),
            "所属公司": f"{fake.company()}有限公司",
            "品牌logo（最多1张）": f"https://example.com/logos/{fake.uuid4()}.png",
            "品牌icon（最多1张）": f"https://example.com/icons/{fake.uuid4()}.svg",
            "门店照片（最多30张）": ", ".join([
                f"https://example.com/stores/{fake.uuid4()}.jpg"
                for _ in range(random.randint(3, 10))
            ]),
            "品牌简介": " ".join(fake.sentences(nb=3)),
            "一级业态": primary_business,
            "二级业态": secondary_business
        }
        brands.append(brand)

    return brands


def write_brand_data_to_excel(template_path, output_path, num_records=100):
    """将品牌数据写入Excel模板"""
    try:
        # 生成随机品牌数据
        brand_data = generate_random_brand_data(num_records)

        # 加载模板文件
        wb = load_workbook(template_path)

        # 获取Sheet1
        ws = wb['Sheet1']

        # 查找数据开始行（跳过标题行）
        start_row = 3

        # 清除现有数据（保留标题）
        for row in range(start_row, ws.max_row + 1):
            for col in range(1, 14):  # 清除前13列
                ws.cell(row=row, column=col).value = None

        # 写入新数据
        for row_idx, brand in enumerate(brand_data, start=start_row):
            ws.cell(row=row_idx, column=1).value = brand["*品牌名称"]
            ws.cell(row=row_idx, column=2).value = brand["一级所属行业"]
            ws.cell(row=row_idx, column=3).value = brand["二级所属行业"]
            ws.cell(row=row_idx, column=4).value = brand["*品牌类型"]
            ws.cell(row=row_idx, column=5).value = brand["成立时间"]
            ws.cell(row=row_idx, column=6).value = brand["发源地"]
            ws.cell(row=row_idx, column=7).value = brand["所属公司"]
            ws.cell(row=row_idx, column=8).value = brand["品牌logo（最多1张）"]
            ws.cell(row=row_idx, column=9).value = brand["品牌icon（最多1张）"]
            ws.cell(row=row_idx, column=10).value = brand["门店照片（最多30张）"]
            ws.cell(row=row_idx, column=11).value = brand["品牌简介"]
            ws.cell(row=row_idx, column=12).value = brand["一级业态"]
            ws.cell(row=row_idx, column=13).value = brand["二级业态"]

            # 设置自动换行格式
            for col in [10, 11]:  # 门店照片和品牌简介列需要自动换行
                ws.cell(row=row_idx, column=col).alignment = Alignment(wrap_text=True)

        # 自动调整列宽
        for col in range(1, 14):
            column_letter = get_column_letter(col)
            max_length = 0

            # 获取列标题
            header = ws.cell(row=4, column=col).value
            if header:
                max_length = len(str(header))

            # 获取列内容最大长度
            for row in range(start_row, start_row + len(brand_data)):
                cell_value = ws.cell(row=row, column=col).value
                if cell_value:
                    # 对于多行文本内容，取最长行
                    lines = str(cell_value).split('\n')
                    for line in lines:
                        if len(line) > max_length:
                            max_length = len(line)

            # 设置列宽（略微宽松）
            adjusted_width = max_length + 3
            ws.column_dimensions[column_letter].width = min(adjusted_width, 50)

        # 保存到新文件
        wb.save(output_path)
        print(f"✅ 成功生成 {len(brand_data)} 条品牌数据")
        print(f"💾 文件已保存至: {output_path}")
        return True

    except Exception as e:
        print(f"❌ 处理文件时发生错误: {e}")
        print("⚠️ 尝试创建新模板并写入数据...")

        # 创建新的工作簿
        wb = load_workbook()

        # 创建Sheet1
        ws = wb.active
        ws.title = "Sheet1"

        # 添加标题行
        headers = [
            "*品牌名称", "一级所属行业", "二级所属行业", "*品牌类型", "成立时间",
            "发源地", "所属公司", "品牌logo（最多1张）", "品牌icon（最多1张）",
            "门店照片（最多30张）", "品牌简介", "一级业态", "二级业态"
        ]
        for col_idx, header in enumerate(headers, start=1):
            ws.cell(row=4, column=col_idx, value=header)

        # 生成随机品牌数据
        brand_data = generate_random_brand_data(num_records)

        # 写入数据
        for row_idx, brand in enumerate(brand_data, start=5):
            ws.cell(row=row_idx, column=1).value = brand["*品牌名称"]
            ws.cell(row=row_idx, column=2).value = brand["一级所属行业"]
            ws.cell(row=row_idx, column=3).value = brand["二级所属行业"]
            ws.cell(row=row_idx, column=4).value = brand["*品牌类型"]
            ws.cell(row=row_idx, column=5).value = brand["成立时间"]
            ws.cell(row=row_idx, column=6).value = brand["发源地"]
            ws.cell(row=row_idx, column=7).value = brand["所属公司"]
            ws.cell(row=row_idx, column=8).value = brand["品牌logo（最多1张）"]
            ws.cell(row=row_idx, column=9).value = brand["品牌icon（最多1张）"]
            ws.cell(row=row_idx, column=10).value = brand["门店照片（最多30张）"]
            ws.cell(row=row_idx, column=11).value = brand["品牌简介"]
            ws.cell(row=row_idx, column=12).value = brand["一级业态"]
            ws.cell(row=row_idx, column=13).value = brand["二级业态"]

        # 保存新文件
        wb.save(output_path)
        print(f"✅ 已创建新模板并写入 {len(brand_data)} 条品牌数据")
        return True


# 文件路径配置
output_id = fake.uuid4()
template_path = '/Users/xaioyang/Downloads/品牌导入模版 (1).xlsx'
output_path = f'/Users/xaioyang/Downloads/{output_id}.xlsx'

# 生成随机数据并写入Excel
write_brand_data_to_excel(template_path, output_path, num_records=10)

print("\n操作完成！")