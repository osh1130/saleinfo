import pandas as pd

def export_to_excel(data, excel_file):
    """
    将折扣数据导出到Excel文件
    Args:
        data (dict): 包含折扣数据的字典
        excel_file (str): 导出的Excel文件名
    """
    # 将数据转换为DataFrame
    df = pd.DataFrame.from_dict({(i, j): data[i][j]
                                 for i in data.keys()
                                 for j in data[i].keys()},
                                orient='index')

    # 导出DataFrame到Excel文件
    df.to_excel(excel_file, index_label=['Brand', 'Model'])
