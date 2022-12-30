from data_get import img_data
from nlptoolsjp.file_system import *
from glob import glob
import os

existed_file = [os.path.splitext(os.path.basename(file))[0] for file in glob("image/*.jpg")]
shop_data = file_load("shop_data_v2.json")
for name,shop in shop_data.items():
    if name in existed_file:
        continue
    shop_url = shop["url"]
    try:
        img = img_data(shop_url)
        if img.status_code == 200:
            with open(f"image/{name}.jpg", "wb") as f:
                f.write(img.content)
    except:
        print(name,shop_url)
        continue