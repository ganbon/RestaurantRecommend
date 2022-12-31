from system.shop import Shop
from nlptoolsjp.file_system import *


shop_data = file_load("data/shop_data_v2.json")
SHOP_DATA = [Shop(shop_data=shop) for name,shop in shop_data.items()]