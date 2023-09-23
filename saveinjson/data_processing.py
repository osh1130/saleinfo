import json
import os
import multiprocessing
import os


current_directory = os.path.dirname(os.path.abspath(__file__))

# 创建一个全局锁
file_lock = multiprocessing.Lock()
def load_discount_data():
    with open(current_directory+'//discount_data.json', 'r') as json_file:
        discount_data = json.load(json_file)
    return discount_data

def add_discount(brand, model, channel, discount, discount_data):
    if brand not in discount_data:
        discount_data[brand] = {}
    if model not in discount_data[brand]:
        discount_data[brand][model] = {}
    discount_data[brand][model][channel] = discount

# def save_discount_data(discount_data):
#     with open('D:/0n3/sale/discount_data.json', 'w') as json_file:
#         json.dump(discount_data, json_file)


def save_discount_data(discount_data):
    # 使用临时文件进行写入，以避免并发问题
    # 使用文件锁
    with file_lock:
        # 先备份原始数据
        original_data = load_discount_data()

        # 将新数据合并到原始数据中
        original_data.update(discount_data)

        # 保存合并后的数据
        with open(current_directory+'//discount_data.json', 'w') as json_file:
            json.dump(original_data, json_file, indent=4)
