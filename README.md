# SaleInfo Project

SaleInfo is a Python project for web scraping and storing mobile phone discount data from different channels. The project is organized into several modules to handle data scraping, processing, export to Excel, and database integration.

## Project Structure

The project is organized as follows:

project_folder/
├── discount_data.json # Stores brand, model, and discount information in a JSON file
├── spiders/
│ ├── one_spider.py # Spider for the One channel
│ ├── 2degrees_spider.py # Spider for the 2Degrees channel
│ ├── spark_spider.py # Spider for the Spark channel
├── data_processing.py # Module for data loading, modification, and saving JSON data
├── excel_export.py # Module for exporting JSON data to Excel
├── database.py # Module for database operations, including connection, data insertion, and querying

## git clone [https://github.com/your_username/SaleInfo.git](https://github.com/osh1130/saleinfo.git)
Install the required Python libraries:
pip install -r requirements.txt

### Modify the spider scripts (one_spider.py, 2degrees_spider.py, spark_spider.py) to specify the URLs and scraping logic for each channel.

### Run the spider scripts to collect discount data(in main):
python one_spider.py
python 2degrees_spider.py
python spark_spider.py
### Data will be stored in discount_data.json(in main).

### To export data to an Excel file(in main), run:
python excel_export.py

### To integrate with a MySQL database, modify the database.py script with your database connection details and execute the necessary functions.(in main)
