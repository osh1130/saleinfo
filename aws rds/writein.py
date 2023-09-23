from datetime import datetime
import pymysql
import json

from saveinjson.data_processing import load_discount_data

# AWS RDS 数据库连接配置
host = 'saleinfo.c39emc4fhkii.us-east-1.rds.amazonaws.com'  # 替换成你的 AWS RDS 数据库端点
port = 3306
user = 'root'
password = '12345678'
database = 'saleinfo'

# 建立数据库连接
conn = pymysql.connect(host=host, port=port, user=user, password=password, database=database)
cursor = conn.cursor()

# 打开JSON文件并加载数据
data = load_discount_data()

# 遍历JSON数据并将其插入到数据库
for brand, models in data.items():
    # 查询是否已存在相同品牌
    check_brand_query = "SELECT brand_id FROM brands WHERE brand_name = %s"
    cursor.execute(check_brand_query, (brand,))
    existing_brand = cursor.fetchone()
    if not existing_brand:
        # 插入品牌数据
        insert_brand_query = "INSERT INTO brands (brand_name) VALUES (%s)"
        cursor.execute(insert_brand_query, (brand,))
        conn.commit()  # 提交品牌数据插入
        brand_id = cursor.lastrowid  # 获取刚插入的品牌的ID
    else:
        brand_id = existing_brand[0]

    for model, details in models.items():
        # 查询是否已存在相同model
        check_model_query = "SELECT model_id FROM models WHERE model_name = %s"
        cursor.execute(check_model_query, (model,))
        existing_model = cursor.fetchone()
        if not existing_model:
            # 插入型号数据或更新已存在的记录，包括型号名称
            insert_model_query = "INSERT INTO models (model_name, brand_id, original_price) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE model_name = VALUES(model_name), original_price = VALUES(original_price)"
            cursor.execute(insert_model_query, (model, brand_id, details.get("original_price")))
            conn.commit()  # 提交型号数据插入
            model_id = cursor.lastrowid  # 获取刚插入的型号的ID
        else:
            model_id = existing_model[0]  # 如果型号已存在，获取型号的ID

        # 插入折扣信息数据
        insert_discount_query = "INSERT INTO discounts (brand_id, model_id, channel, discount_amount, date) VALUES (%s, %s, %s, %s, %s)"
        date = datetime.now().date()

        # 尝试插入 "2degrees" 数据，如果发生重复插入错误则忽略
        try:
            cursor.execute(insert_discount_query, (brand_id, model_id, "2degrees", details.get("2degrees"), date))
        except pymysql.IntegrityError as e:
            if e.args[0] == 1062:  # 错误码 1062 表示重复插入
                pass  # 忽略重复插入错误
            else:
                raise  # 如果是其他类型的 IntegrityError，则继续抛出异常

        # 尝试插入 "One NZ" 数据，如果发生重复插入错误则忽略
        try:
            cursor.execute(insert_discount_query, (brand_id, model_id, "One NZ", details.get("One NZ"), date))
        except pymysql.IntegrityError as e:
            if e.args[0] == 1062:  # 错误码 1062 表示重复插入
                pass  # 忽略重复插入错误
            else:
                raise  # 如果是其他类型的 IntegrityError，则继续抛出异常

        # 尝试插入 "Spark" 数据，如果发生重复插入错误则忽略
        try:
            cursor.execute(insert_discount_query, (brand_id, model_id, "Spark", details.get("Spark"), date))
        except pymysql.IntegrityError as e:
            if e.args[0] == 1062:  # 错误码 1062 表示重复插入
                pass  # 忽略重复插入错误
            else:
                raise  # 如果是其他

        conn.commit()  # 提交折扣信息数据插入

# 关闭数据库连接
cursor.close()
conn.close()
