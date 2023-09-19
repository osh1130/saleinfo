import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import data_processing

chrome_options = Options()
chrome_options.add_argument("--headless")  # 设置为headless模式，不显示浏览器窗口
chrome_options.add_argument("--disable-gpu")  # 禁用GPU加速，可避免一些兼容性问题
driver = webdriver.Chrome(options=chrome_options)

discount_data = data_processing.load_discount_data()

def read(url):
    driver.get(url)
    time.sleep(6)
    html = driver.page_source
    bf = BeautifulSoup(html, 'html.parser')
    return bf, driver

def devices(bf,brand):
    devices = bf.find_all('div', {'data-regionid': 'productGallery'})
    for device in devices:
        model = device.find('h5').text
        price = device.find('p',{"title": "Device only price"}).text
        original_price = price.split('$')[1].replace(',','').split(".")[0]
        saving = device.find('p',{'class':"sc-834c5326-3 sc-834c5326-13 fwTbqt dsioqg"})
        # datail = device.find('a')['href']
        # datail,driver = read(datail)
        # storage = datail.find('id',{'id','device-storage'})
        if saving:
            saving = saving.text
            discount=saving.split(" ")[1].split('$')[1].replace(',','')
        else:
            discount = 0
        itemsql = [model, discount, brand, original_price]
        writeinjson(itemsql)

def writeinjson(itemsql):
    model, discount, brand, original_price = itemsql
    if brand not in discount_data:
        discount_data[brand] = {}
    if model not in discount_data[brand]:
        discount_data[brand][model] = {}
    discount_data[brand][model]["original_price"] = original_price
    # 使用模块中的函数添加折扣信息
    data_processing.add_discount(brand, model, "Spark", discount, discount_data)



# 定义品牌和对应的URL字典 (Spark 渠道)
spark_brands_and_urls = {
    "Apple": "https://www.spark.co.nz/online/shop/handsets/?brand=apple",
    "Samsung": "https://www.spark.co.nz/online/shop/handsets/?brand=samsung",
    "OPPO": "https://www.spark.co.nz/online/shop/handsets/?brand=oppo",
}

def crawl_spark(spark_brands_and_urls):
    # 遍历 Spark 渠道的品牌和URL字典，爬取折扣信息
    for brand, url in spark_brands_and_urls.items():
        bf = read(url)
        devices(bf, brand)  # 指定渠道为 "Spark"

# 调用 Spark 渠道的折扣信息爬取函数
#crawl_spark(spark_brands_and_urls)

# 保存折扣数据到JSON文件
data_processing.save_discount_data(discount_data)

# 关闭WebDriver
driver.quit()

