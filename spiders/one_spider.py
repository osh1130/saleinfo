import os
import sys
import time
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
sys.path.append('F:\\saleinfo')

import data_processing

discount_data = data_processing.load_discount_data()


chrome_options = Options()
chrome_options.add_argument("--headless")  # 设置为headless模式，不显示浏览器窗口
chrome_options.add_argument("--disable-gpu")  # 禁用GPU加速，可避免一些兼容性问题
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
chrome_driver_path = "F:\chromedriver-win64\chromedriver-win64\chromedriver.exe"  # 指定你下载的匹配版本的 ChromeDriver 路径
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

def read(url):
    driver.get(url)
    #time.sleep(6)
    while True:
        try:
            # 使用 By.CLASS_NAME 选择器找到按钮
            button = WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.CLASS_NAME, "vf-product-listings-paginator__button"))
            )
            # 滚动到按钮，确保按钮在窗口中
            driver.execute_script("arguments[0].scrollIntoView(true);", button)
            time.sleep(1)

            # 使用 WebDriverWait 来确保按钮变得可点击
            WebDriverWait(driver, 60).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "vf-product-listings-paginator__button"))
            )
            # 使用 JavaScript 执行点击操作
            driver.execute_script("arguments[0].click();", button)

            # 暂停，等待页面加载完成新的内容
            WebDriverWait(driver, 60).until(EC.staleness_of(button))
        except TimeoutException:
            break

    html = driver.page_source
    bf = BeautifulSoup(html, "html.parser")
    #devices = soup.find_all('div', {'data-portal-key': 'portal'})
    return bf


def devices(bf):
    devices = bf.find_all('div', {'data-portal-key': 'portal'})
    for device in devices:
        brand = device.select(".styled__TitleWrapper-sc-v1pv3k-0 h1.kaZFrM")[0].text
        model = device.select(".styled__TitleWrapper-sc-v1pv3k-0 h2.cA-DiIP")[0].text
        saving = device.select(".dHGgTl .erzlYW")
        discount = saving[0].text.split(" ")[1].split('$')[1] if saving else 0
        itemsql = [model, discount, brand]
        writeinjson(itemsql)

def writeinjson(itemsql):
    model, discount, brand = itemsql
    # 使用模块中的函数添加折扣信息
    data_processing.add_discount(brand, model, "One NZ", discount, discount_data)
    #print(discount_data[brand][model])

# 使用函数
url = "https://one.nz/online-shop/mobile/product-listing/?_bc_fsnf=1&sort=featured&planType=onAccount"
def crawl_One():
    bf = read(url)
    devices(bf)
    print("one nz done!")
    # 保存折扣数据到JSON文件
    data_processing.save_discount_data(discount_data)

    # 关闭WebDriver
    driver.quit()

#if __name__ == '__main__':
crawl_One()





