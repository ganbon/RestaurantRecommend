from nlptoolsjp.text_get import *
from nlptoolsjp.file_system import *


# soup = scraping_obj("https://tabelog.com/cat_lst/")
# tag = soup.find("div",class_="rst-catlst")
# _,title = scraping_url(soup=tag)
# file_create(title,"../data/rule.txt")
# print(title)
# exit(1)
genre_dict = {}
genre_text = file_load("../data/rule.txt")
kind = None
id_count = 0
for g in genre_text:
    if kind == None:
        kind = g
        genre_dict[g] = {"id":id_count,"関連":[]}
    elif g=="":
        genre_dict[kind]["関連"] = list(set(genre_dict[kind]["関連"]))
        kind=None
        id_count += 1
    else:
        genre_dict[kind]["関連"].append(g)
file_create(genre_dict,"../data/genre_rule.json")


