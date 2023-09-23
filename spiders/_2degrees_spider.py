import sys
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
sys.path.append('F:\\saleinfo')
import data_processing

chrome_options = Options()
chrome_options.add_argument("--headless")  # 设置为headless模式，不显示浏览器窗口
chrome_options.add_argument("--disable-gpu")  # 禁用GPU加速，可避免一些兼容性问题
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
chrome_driver_path = "F:\chromedriver-win64\chromedriver-win64\chromedriver.exe"  # 指定你下载的匹配版本的 ChromeDriver 路径
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

discount_data = data_processing.load_discount_data()

def read(url):
    driver.get(url)
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class="tile-layout-col mt-5 d-flex"]')))
    html = driver.page_source
    bf = BeautifulSoup(html, 'html.parser')
    return bf

def devices(bf,brand):
    devices = bf.find_all('div', {'class': 'tile-layout-col mt-5 d-flex'})
    for device in devices:
        model = device.find('span', {"data-test-id": "GalleryCard-title"}).find('strong').text
        saving = device.find('span', {'data-test-id': "GalleryCard-ribbon-tag"})
        if saving:
            saving = saving.find('strong').text
            discount = saving.split(" ")[1].split('$')[1].replace(',', '')
        else:
            discount = 0
        itemsql = [model, discount, brand]
        writeinjson(itemsql)

def writeinjson(itemsql):
    model, discount, brand = itemsql
    # 使用模块中的函数添加折扣信息
    data_processing.add_discount(brand, model, "2degrees", discount, discount_data)
    #print(discount_data[brand][model])

degrees_brands_and_urls = {
    "Apple": "https://www.2degrees.nz/shop/browse?filterKey1=itemBrand&filterValue1=Apple&filterKey2=itemCategory&filterValue2=Mobile+Phones",
    "Samsung": "https://www.2degrees.nz/shop/browse?filterKey1=itemBrand&filterValue1=Samsung&filterKey2=itemCategory&filterValue2=Mobile+Phones",
    "OPPO": "https://www.2degrees.nz/shop/browse?filterKey1=itemBrand&filterValue1=OPPO&filterKey2=itemCategory&filterValue2=Mobile+Phones",
}

def crawl_2degrees(degrees_brands_and_urls):
    # 遍历品牌和URL字典，爬取折扣信息
    for brand, url in degrees_brands_and_urls.items():
        bf = read(url)
        devices(bf, brand)

    print("2d done!")

    # 保存折扣数据到JSON文件
    data_processing.save_discount_data(discount_data)

    # 关闭WebDriver
    driver.quit()

if __name__ == '__main__':
    crawl_2degrees(degrees_brands_and_urls)




