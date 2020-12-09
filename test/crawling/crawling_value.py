from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from tqdm import tqdm


def get_images(keyword):
    #웹 접속: 네이버 이미지 접속
    print('접속중')
    driver = webdriver.Chrome('chromedriver.exe')
    driver.implicitly_wait(30)

    url = "https://www.google.com/search?q={}&sxsrf=ALeKk002UWJb871OUGYuECHnS0GTt34WrA:1605860114292&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjX_q6N15DtAhVVL6YKHSfFCgoQ_AUoAnoECA0QBA&biw=958&bih=959".format(keyword)
    driver.get(url)

    #페이지 스크롤 다운 
    body = driver.find_element_by_css_selector("body")

    for i in range(20):
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(1)
 

    #이미지 링크 수집 
    imgs = driver.find_elements_by_css_selector("img.rg_i")

    
    
    # print(imgs)
    result = []
    
    for img in tqdm(imgs):
        if img.get_attribute('src') != None:
            if 'http' in img.get_attribute('src'):
                result.append(img.get_attribute('src'))
    print(result)
    driver.close()
    
    print('수집완료')

    #저장 디렉토리 생성
    print('디렉토리 생성')
    import os

    if not os.path.isdir("./{}".format('highvaluecolor')):
        os.makedirs("./{}".format('highvaluecolor'))

    #다운로드 
    print('다운로드')
    from urllib.request import urlretrieve
    for index , link in tqdm(enumerate(result)):
        start = link.rfind(".")
        end = link.rfind("&")
        print(link[start:end])
        filetype = link[start:end]
        #index 기준으로 업시켜줘야 중복 안됨 @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        urlretrieve(link, './{}/{}{}{}'.format('highvaluecolor','highvaluecolor',index+931,'.jpg'))






if __name__ == '__main__':
    keyword = input('insert keyword: ')
    # keyword.decode('utf-8')
    get_images(keyword)



