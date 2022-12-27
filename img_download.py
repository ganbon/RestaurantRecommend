from data_get import img_data
from nlptoolsjp.file_system import *

shop_data = file_load("shop_data.json")
for shop in shop_data:
    shop_name = shop["店名"]
    shop_url = shop["url"]
    img = img_data(shop_url)
    if img.status_code == 200:
        with open(f"image/{shop_name}.jpg", "wb") as f:
            f.write(img.content)