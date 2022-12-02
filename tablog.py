from data_get import tab_scraping
import time
from datetime import datetime
from glob import glob
from nlptoolsjp.file_system import *
from nlptoolsjp.text_get import *


data_path = file_load("csv_data/shop.csv")
# print(data_path.index)
url_list = data_path.index
shop_list = data_path["店名"].tolist()
loaded_list = [file_load(file)["url"] for file in glob("tablog_data/*.json")]
print(datetime.now())
for url,shop in zip(url_list,shop_list):
    if url in loaded_list:
        # print(shop+" is loaded")
        continue
    try:
        print(shop)
        data = tab_scraping(url)
    except:
        print(url)
        print(datetime.now())
        exit(1)
    if data["店名"] is not None:
        file_create(data,f"tablog_data/{shop}.json")
        print(shop+" is ok!")
    time.sleep(10)
