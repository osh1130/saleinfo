import json
import os
from datetime import datetime
from saveinjson import data_processing
import subprocess
from create_excel import excel_export

#chromedriver_autoinstaller.install()
# 创建一个空字典
empty_dict = {}

#打开 JSON 文件，清空内容
with open('saveinjson/discount_data.json', 'w') as json_file:
    json.dump(empty_dict, json_file)

# 关闭文件
json_file.close()

# 运行第一个脚本
#subprocess.run(["python", "spiders/spark_spider.py"])


#运行第二个脚本
#subprocess.run(["python", "spiders/one_spider.py"])

#运行第三个脚本
#subprocess.run(["python", "spiders/_2degrees_spider.py"])

# 加载折扣数据从JSON文件，或者使用你已有的数据
discount_data = data_processing.load_discount_data()
current_date = datetime.now().date()
current_directory = os.path.dirname(os.path.abspath(__file__))
name = current_directory + '//create_excel//'+ 'SaleInfo-%s.xlsx' % (str(current_date))
excel_export.export_to_excel(discount_data, name)
print("excel done")

#subprocess.run(["python", "aws rds/writein.py"])
