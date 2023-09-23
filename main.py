import json
import time
from datetime import datetime
import data_processing
import subprocess
import excel_export

# from spiders.one_spider import crawl_One
# from spiders._2degrees_spider import crawl_2degrees
# from spiders.spark_spider import crawl_spark

#chromedriver_autoinstaller.install()
# 创建一个空字典
empty_dict = {}

#打开 JSON 文件，清空内容
with open('discount_data.json', 'w') as json_file:
    json.dump(empty_dict, json_file)

# 关闭文件
json_file.close()

# 运行第一个脚本
subprocess.run(["python", "spiders\spark_spider.py"])


#运行第二个脚本
subprocess.run(["python", "spiders\one_spider.py"])

#运行第三个脚本
subprocess.run(["python", "spiders\_2degrees_spider.py"])

# 加载折扣数据从JSON文件，或者使用你已有的数据
discount_data = data_processing.load_discount_data()
current_date = datetime.now().date()
name = 'SaleInfo-%s.xlsx' % (str(current_date))
excel_export.export_to_excel(discount_data, name)

subprocess.run(["python", "writeinsql.py"])
