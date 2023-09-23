from datetime import datetime

import pandas as pd

import data_processing


def export_to_excel(data, excel_file):
    """
    将折扣数据导出到Excel文件
    Args:
        data (dict): 包含折扣数据的字典
        excel_file (str): 导出的Excel文件名
    """
    # 将数据转换为DataFrame
    # 创建一个空的 DataFrame
    df = pd.DataFrame(columns=["Brand", "Model", "Original Price", "Spark", "One NZ", "2degrees"])

    # 遍历 JSON 数据并填充 DataFrame
    for brand, models in data.items():
        for model, details in models.items():
            original_price = details.get("original_price", "")
            spark = details.get("Spark", "")
            one_nz = details.get("One NZ", "")
            two_degrees = details.get("2degrees", "")
            df = df._append(
                {"Brand": brand, "Model": model, "Original Price": original_price, "Spark": spark, "One NZ": one_nz,
                 "2degrees": two_degrees}, ignore_index=True)

    # 导出DataFrame到Excel文件
    df.to_excel(excel_file, index=False)

# discount_data = data_processing.load_discount_data()
# current_date = datetime.now().date()
# name = 'SaleInfo-%s.xlsx' % (str(current_date))
# export_to_excel(discount_data, name)