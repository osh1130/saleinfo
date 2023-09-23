import pymysql


conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', database='saleinfo')
cursor = conn.cursor()


# 创建品牌表
create_brands_table = '''
CREATE TABLE IF NOT EXISTS brands (
    brand_id INT AUTO_INCREMENT PRIMARY KEY,
    brand_name VARCHAR(255) NOT NULL,
    UNIQUE (brand_name)  -- 在品牌名称上设置唯一约束
);
'''

# 创建型号表
create_models_table = '''
CREATE TABLE IF NOT EXISTS models (
    model_id INT AUTO_INCREMENT PRIMARY KEY,
    model_name VARCHAR(255) NOT NULL,
    brand_id INT,
    original_price DECIMAL(10, 2),
    FOREIGN KEY (brand_id) REFERENCES brands (brand_id),
    UNIQUE (model_name, brand_id)  -- 在型号名称和品牌 ID 上设置唯一约束
);
'''

# 创建折扣信息表
create_discounts_table = '''
CREATE TABLE IF NOT EXISTS discounts (
    discount_id INT AUTO_INCREMENT PRIMARY KEY,
    brand_id INT,
    model_id INT,
    channel VARCHAR(255),
    discount_amount FLOAT,
    date DATE,
    FOREIGN KEY (brand_id) REFERENCES brands (brand_id),
    FOREIGN KEY (model_id) REFERENCES models (model_id),
    UNIQUE (model_id, channel, date)  -- 在(model_id, channel, date)列上设置唯一约束
);
'''

# 执行创建表的SQL语句
cursor.execute(create_brands_table)
cursor.execute(create_models_table)
cursor.execute(create_discounts_table)

# 提交事务
conn.commit()

cursor.close()
conn.close()
