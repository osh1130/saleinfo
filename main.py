from datetime import datetime
import data_processing
from spiders._2degrees_spider import degrees_brands_and_urls, crawl_2degrees
from spiders.one_spider import crawl_One
from spiders.spark_spider import spark_brands_and_urls, crawl_spark
import excel_export  # 导入自定义模块

data_processing.clear_discount_data()
print(data_processing.load_discount_data())

# 执行 Spark 渠道的折扣信息爬取
crawl_spark(spark_brands_and_urls)

# 执行 2degrees 渠道的折扣信息爬取
crawl_2degrees(degrees_brands_and_urls)

# 执行 One NZ 渠道的折扣信息爬取
crawl_One()

# 加载折扣数据从JSON文件，或者使用你已有的数据
discount_data = data_processing.load_discount_data()
current_date = datetime.now().date()
name = 'SaleInfo-%s.xlsx' % (str(current_date))
excel_export.export_to_excel(discount_data, name)

