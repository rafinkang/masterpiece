'''
쿨톤, 웜톤, 비비드, 파스텔 이미지 크롤링
'''

from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint
from pathlib import Path

for i in range(1, 265): # 웹 페이지 수
    url = "https://colorpalettes.net/category/contrasting-color/page/" + str(i) + "/" # 웹 url
    res = requests.get(url)

    res.raise_for_status()

    soup = bs(res.text, "lxml")
    img_list = soup.find("div", attrs={"class", "nointernal"}).find_all("img")

    for img in img_list:
        path = img.attrs["src"]
        res3 = requests.get(path)

        img_dir = "crawling/contrasting" # 저장 directory
        img_name = path.split("/")[-1]

        Path(img_dir).mkdir(parents = True, exist_ok = True)
        with open(img_dir + "/" + img_name, "wb") as f: # 이미지 저장
            f.write(res3.content)
        
        print(img_name)