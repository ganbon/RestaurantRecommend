from nlptoolsjp.text_get import *
import time

def hotpepper_scraping(url):
    data = {"url":url,"店名":None,"予算":None,"ジャンル":None,
            "住所":None,"営業日":None,"評価":0,
            "来店シーン":None,"口コミ":[]}
    comment_url = url+"report/"
    soup = scraping_obj(url)
    time.sleep(10)
    title = soup.find("h1",class_="shopName")
    data["店名"] = title.text
    chage = soup.find("span",class_="shopInfoBudgetDinner")
    if chage != None:
        data["予算"] = chage.text
    date = soup.find("dd",class_="shopHour")
    if date != None:
        data["営業日"] = date.text
    kind = soup.find("div",class_="crown")
    if kind != None:
        data["ジャンル"] = kind.text
    value = soup.find("span",class_="ratingScoreValue rating3")
    if value != None:
        data["評価"] = float(value.text)
    scene = soup.find("ul",class_="sceneTextList")
    if scene != None:
        data["来店シーン"] = scene.text
    place = soup.find("address")
    if place != None:
        data["住所"] = place.text
    for i in range(1,100,5):
        if i!=1:
            _comment_url = comment_url+f"list_{i}/"
        else:
            _comment_url = comment_url
        url_list = scraping_url(_comment_url,"arrowLink")
        time.sleep(10)
        if url_list == []:
            break
        for j,com_url in enumerate(url_list):
            com = scraping_obj("https://www.hotpepper.jp"+com_url)
            comment = com.find("span",class_="text")
            data["口コミ"].append(comment.text)
            time.sleep(10)
    return data


def tab_scraping(url):
    data = {"url":url,"店名":None,"予算":"","予算(user)":"","ジャンル":None,
            "住所":None,"営業時間":None,"定休日":None,"評価":0,
            "口コミ":[]}
    soup = scraping_obj(url)
    if soup.find("a",class_="rst-status-badge-red__text") is not None:
        if soup.find("a",class_="rst-status-badge-red__text").text=="閉店":
            return data
    try:
        shop_data = soup.select("#rst-data-head")[0]
    except:
        return data
    comment_url = url+"dtlrvwlst//COND-0/smp0/?smp=0&lc=0&rvw_part=all"
    time.sleep(20)
    title_root = soup.find("h2",class_="display-name")
    title = title_root.find("span")
    data["店名"] = title.text
    chage_root = shop_data.find_all("div",class_="rstinfo-table__budget")
    chage_dinner1 = chage_root[0].find("em",class_="gly-b-dinner")
    chage_lunch1 = chage_root[0].find("em",class_="gly-b-lunch")
    if len(chage_root) >= 2:
        chage_dinner2 = chage_root[1].find("em",class_="gly-b-dinner")
        chage_lunch2 = chage_root[1].find("em",class_="gly-b-lunch")
        if chage_dinner2 != None:
            data["予算(user)"] += chage_dinner2.text
        if chage_lunch2 != None:
            data["予算(user)"] += chage_lunch2.text
    if chage_dinner1 != None:
        data["予算"] += chage_dinner1.text
    if chage_lunch1 != None:
        data["予算"] += chage_lunch1.text
    date = shop_data.find_all("p",class_="rstinfo-table__subject-text")
    if date != []:
        data["営業時間"] = date[0].text
        if len(date) > 1:
            data["定休日"] = date[1].text
    kind = shop_data.find_all("td")
    if kind[1] != None:
        data["ジャンル"] = kind[1].text
    value = soup.find("span",class_="rdheader-rating__score-val-dtl")
    if value != None and value.text != "-":
        data["評価"] = float(value.text)
    place = soup.find("p",class_="rstinfo-table__address")
    if place != None:
        data["住所"] = place.text
    for i in range(1,11):
        _comment_url = comment_url+f"&PG={i}"
        url_list,_ = scraping_url(_comment_url,"rvw-simple-item__title-target")
        # print(url_list)
        time.sleep(20)
        if url_list == []:
            break
        for j,com_url in enumerate(url_list):
            com = scraping_obj("https://tabelog.com"+com_url)
            comment_tag = com.find("div",class_="rvw-item__rvw-comment rvw-item__rvw-comment--custom")
            if comment_tag is None:
                continue
            comment = comment_tag.find("p")
            data["口コミ"].append(comment.text)
            time.sleep(10)
    return data


def user_data(url):
    data_list = []
    soup = scraping_obj(url)
    time.sleep(10)
    sub_soup = soup.find_all("div",class_="rvw-item rvw-item--simple rvw-item--rvwlst js-rvw-item")
    for s in sub_soup:
        data = {"url":url,"shop_url":None,"店名":None,"訪問日時":None,"評価":{"昼":0,"夜":0}}
        shop = s.find("a",class_="simple-rvw__rst-name-target")
        data["shop_url"] = shop.get("href")
        data["店名"] = shop.text
        visited = s.find("span",class_="p-preview-visit__visited-date")
        if visited is not None:
            data["訪問日時"] = visited.text
        review = s.find_all("b",class_="c-rating-v2__val c-rating-v2__val--strong")
        lunch = s.find("span",class_="c-rating-v2__time c-rating-v2__time--lunch")
        dinner = s.find("span",class_="c-rating-v2__time c-rating-v2__time--dinner")
        if len(review) > 1:
            if dinner is not None and review[0].text != '-':
                data["評価"]["夜"] = float(review[0].text)
                if review[1].text != '-':
                    data["評価"]["昼"] = float(review[1].text)
            elif lunch is not None and review[0].text != '-':
                data["評価"]["昼"] = float(review[0].text)
        elif len(review) == 1:
            if lunch is not None and review[0].text != '-':
                data["評価"]["昼"] = float(review[0].text)
            if dinner is not None and review[0].text != '-':
                data["評価"]["夜"] = float(review[0].text)
        data_list.append(data)
    return data_list





if __name__=="__main__":
    tab_url = "https://tabelog.com/kagawa/A3701/A370101/37005793/"
    tab_url2 = "https://tabelog.com/kagawa/A3701/A370101/37006843/"
    tab_url3 = "https://tabelog.com/kagawa/A3701/A370101/37000360/"
    data = tab_scraping(tab_url3)
    print(data)
    # file_create(data,"test.json")