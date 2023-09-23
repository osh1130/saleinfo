import os
import sys
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
# 获取当前脚本文件的目录
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)
sys.path.append(parent_dir)
from saveinjson import data_processing

chrome_options = Options()
chrome_options.add_argument("--headless")  # 设置为headless模式，不显示浏览器窗口
chrome_options.add_argument("--disable-gpu")  # 禁用GPU加速，可避免一些兼容性问题
# 构建相对路径到chromedriver.exe
chrome_driver_path = os.path.join(script_dir, 'chromedriver.exe')
#chrome_driver_path = "F:\saleinfo\spiders\chromedriver.exe"  # 指定你下载的匹配版本的 ChromeDriver 路径
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

discount_data = data_processing.load_discount_data()

def read(url):
    driver.get(url)
    #time.sleep(6)
    # 使用显式等待等待元素加载完成
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-regionid="productGallery"]')))
    html = driver.page_source
    bf = BeautifulSoup(html, 'html.parser')
    return bf

def devices(bf,brand):
    devices = bf.find_all('div', {'data-regionid': 'productGallery'})
    for device in devices:
        model = device.find('h5').text.replace(brand, "").strip()
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
        #print(itemsql)
        writeinjson(itemsql)

def writeinjson(itemsql):
    model, discount, brand, original_price = itemsql
    #discount_data[brand][model]["original_price"] = original_price
    data_processing.add_discount(brand, model, "original_price", original_price, discount_data)
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

    print("spark done!")
    # 保存折扣数据到JSON文件
    data_processing.save_discount_data(discount_data)

    # 关闭WebDriver
    driver.quit()

# 调用 Spark 渠道的折扣信息爬取函数
if __name__ == '__main__':
    crawl_spark(spark_brands_and_urls)