from data_get import tab_scraping
from tqdm import tqdm
from datetime import datetime
from glob import glob
from nlptoolsjp.file_system import *
from nlptoolsjp.text_get import *


data_path = file_load("csv_data/shop.csv")
try:
    closed_data = file_load("csv_data/closed_shop.csv")
except:
    closed_data = pd.DataFrame({"url":[],"店名":[]})
# print(data_path.index)
url_list = data_path["url"].tolist()
shop_list = data_path["店名"].tolist()
loaded_list = [file_load(file)["url"] for file in glob("tablog_data/*.json")]
print(datetime.now())
for url,shop in (zip(tqdm(url_list),shop_list)):
    if url in loaded_list or url in closed_data["url"].tolist():
        # print(shop+" is loaded")
        continue
    try:
        print(shop)
        data = tab_scraping(url)
    except:
        print(url)
        print(datetime.now())
        file_create(closed_data,"csv_data/closed_shop.csv")
        exit(1)
    if data["店名"] is not None:
        file_create(data,f"../data/tablog_data/{shop}.json")
        print(shop+" is ok!")
    else:
        close = pd.DataFrame({"url":[url],"店名":[shop]})
        closed_data = pd.concat([closed_data,close],axis=0)
        closed_data = closed_data.reset_index(drop=True)
    # time.sleep(10)