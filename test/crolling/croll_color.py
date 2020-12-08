import os
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from tqdm import tqdm
import os
from urllib.request import urlretrieve


def get_images(keyword, range_num):
    # 웹 접속 :  네이버 이미지 접속
    print("접속중")

    driver = webdriver.Chrome(
        "D:\workspace\chromedriver_win32\chromedriver.exe")
    driver.implicitly_wait(30)

    # 이미지 링크 리스트
    result = []
    for page in range(1, int(range_num)):
        url = "https://colorpalettes.net/category/{}/page/{}/".format(keyword, page)
        driver.get(url)

        # 이미지 링크수집
        imgs = driver.find_elements_by_css_selector(
            "#boxloop > div.nointernal > div > div > a.vis-desk > img")
        # print(imgs)

        for img in tqdm(imgs):
            img.find_elements
            if 'http' in img.get_attribute('src'):
                result.append(img.get_attribute('src'))

        # time.sleep(0.2)

    # print(result)

    # 저장 디렉토리 생성
    print("폴더 생성")
    if not os.path.isdir("./test/crolling/images/{}".format(keyword)):
        os.makedirs("./test/crolling/images/{}".format(keyword))

    # 다운로드
    print("다운로드 시작")

    for index, link in tqdm(enumerate(result)):
        print(index, link)
        start = link.rfind(".")
        # end = link.rfind("&")
        # print(link[start:end])  -> .jpg, .png, .git ...
        filetype = link[start:]

        # 저장위치, 파일명까지
        urlretrieve(link, './test/crolling/images/{}/{}{}{}'.format(keyword,
                                               keyword, index, filetype))


if __name__ == "__main__":
    keyword = input("폴더명 입력 : ")
    range_num = input("횟수 입력 : ")
    get_images(keyword, range_num)

    # aa = "https://colorpalettes.net/wp-content/uploads/2020/12/color-palette-4267.png"
    # print(aa.rfind("."), aa.rfind('&'))
    # print(aa[aa.rfind("."):])