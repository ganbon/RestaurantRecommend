from nlptoolsjp.text_get import *
import time
from data_get import user_data
from nlptoolsjp.file_system import *
from glob import glob

filename_list = [name.split("\\")[-1] for name in glob("../data/tablog_userdata/*.json")]
data = file_load("../data/user.json")
start_time = time.time()
target_username = None
for url,user in data.items():
    if f"{user}-1.json" in filename_list and user != target_username:
        continue
    for j in range(1,41):
        if j==1:
            user_url = url+"visited_restaurants/list/?pal=kagawa&Srt=D&SrtT=lvd&bookmark_type=1&award_year=2022&review_content_exist=0"
        else:
            user_url = url+f"visited_restaurants/list/?pal=kagawa&Srt=D&SrtT=lvd&bookmark_type=1&award_year=2022&review_content_exist=0&sk=&sw=&PG={j}"
        if f"{user}-{j}.json" in filename_list:
            print(user)
            continue
        data_list = user_data(user_url)
        if data_list == []:
            break
        print(user,j)
        try:
            file_create(data_list,f"../data/tablog_userdata/{user}-{j}.json")
        except:
            file_create(data_list,f"../data/tablog_userdata/{user}-{j}.json")
    end_time = time.time()
    print(user,end_time-start_time)

end_time = time.time()
print(end_time-start_time)