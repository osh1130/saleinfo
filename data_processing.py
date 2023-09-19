import json

def load_discount_data():
    with open('F:/saleinfo/discount_data.json', 'r') as json_file:
        discount_data = json.load(json_file)
    return discount_data

def add_discount(brand, model, channel, discount, discount_data):
    if brand not in discount_data:
        discount_data[brand] = {}
    if model not in discount_data[brand]:
        discount_data[brand][model] = {}
    discount_data[brand][model][channel] = discount

def save_discount_data(discount_data):
    with open('F:/saleinfo/discount_data.json', 'w') as json_file:
        json.dump(discount_data, json_file)
