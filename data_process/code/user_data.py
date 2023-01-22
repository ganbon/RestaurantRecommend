from nlptoolsjp.text_get import *
import time
from nlptoolsjp.file_system import *

start_time = time.time()
url_list = []
title_list = []
for i in range(1,13):
    for j in range(5):
        url = f"https://tabelog.com/rvwrs/rvwr_ranking/kagawa/ranking_lst/{j+1}/2022-{i}"
        u,t = scraping_url(url,"rvwr-intro__name-target")
        print(u,t)
        time.sleep(10)
        url_list += u
        title_list += t
data_list = list(map(list,set(map(tuple,[[u,t] for u,t in zip(url_list,title_list)]))))
data_list = dict(data_list)
file_create(data_list,"../data/user.json")