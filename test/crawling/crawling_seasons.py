import requests
import time
import pyautogui
import pyperclip
import re
from bs4 import BeautifulSoup as bs
from pprint import pprint
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import sys
import cx_Oracle

import pandas as pd
import os

cnt = 0
serial = ""
page = 0

# url = "http://wallpaperswide.com/spring-desktop-wallpapers/page/"
# url = "http://wallpaperswide.com/summer-desktop-wallpapers/page/"
# url = "http://wallpaperswide.com/autumn-desktop-wallpapers/page/"
url = "http://wallpaperswide.com/winter-desktop-wallpapers/page/"


browser = webdriver.Chrome("C:\\Users\\user\\Desktop\\쿠팡\\chromedriver.exe")

try:
    while True:
        page = page +1
        url2 = url+str(page)

        browser.get(url2)

        element_list = browser.find_elements_by_class_name("thumb_img")
        # print(element_list)

        # 1개의 페이지 안에서 크롤링
        for i in element_list:
            image_url = i.get_attribute("src")
            # print(image_url)
            image_url2 = image_url[36:-7]
            # print(image_url2)
            image_url3 = "http://wallpaperswide.com/download/" + image_url2 + "-wallpaper-960x600.jpg"
            # print(image_url3)
            cnt += 1
            image_name = "winter"+"0"*(4-len(str(cnt)))+str(cnt)+".jpg"
                
            # curl 요청
            os.system("curl " + image_url3 + " > "+image_name)
except:
    print("페이지 끝났습니다.")



# for key in keywordlist:
#     csvlist = []

#     cnt = 1
#     page = 1
#     errorcnt = 0
#     errorbreak = 0
#     product_url_list = []

#     keyword = key
#     # print("1")

#     # print("2")

#     # for page in range(1,10):
#     #     for i in range(1,40):
#     for page in range(1,5):
#         print(page,"페이지")

#         # path_product_front = "/html/body/div[2]/section/form/div[2]/div[2]/ul/li["
#         # path_product_count = i
#         # path_product_back = "]"
#         # path_product = path_product_front + str(path_product_count) + path_product_back
#         # # /html/body/div[2]/section/form/div[2]/div[2]/ul/li[1]/a/dl
#         # path_product_name = path_product + "/a/dl/dd/div/div[2]"
#         # path_product_price = path_product + "/a/dl/dd/div/div[3]/div/div[1]/em/strong"
#         # path_product_rocket = path_product + "/a/dl/dd/div/div[3]/div/div[1]/em/span"
#         # path_product_gume = path_product + "/a/dl/dd/div/div[4]/div/span[2]"
#         # path_product_ad = path_product + "/a/dl/dd/div/div[1]"
        
#         # # print(path_product)
        
#         productlist = []
#         while len(productlist) == 0:
#             productlist = browser.find_elements_by_class_name("search-product ")
#             # time.sleep(1)
            
        
#         for pdl in productlist:
#             if '광고' in pdl.text:
#                 print("광고네 건너뛰자")
#                 continue
            
#             product_url = pdl.find_element_by_css_selector('a').get_attribute('href')
#             print(product_url)
#             product_url_list.append(product_url)
#             print(cnt,"번째 상품")
#             cnt += 1
        
        
#         # time.sleep(1)    
#         try:
#             next = browser.find_element_by_css_selector("#searchOptionForm > div.search-wrapper > div.search-content.search-content-with-feedback > div.search-pagination > a.btn-next")
#             next.click()
#             print("다음페이지로~")
#         except:
#             print("다음페이지가 없네")
#             break


#     cnt = 1

#     for product in product_url_list:
#         templist = []
#         browser.get(product)
#         time.sleep(0.5)

#         print( str(cnt),"번째 상품")
#         cnt += 1

#         try:
#             product_name = browser.find_element_by_class_name("prod-buy-header__title")
#         except:
#             # print("에러난듯, 다음상품으로")
#             continue


#         product_name = ""
#         while len(product_name) == 0:
#             # print("이름 가지러들어옴")
#             try:
#                 product_name = browser.find_element_by_class_name("prod-buy-header__title").text
#             except:
#                 product_name = ""
#             print(product_name)
#             templist.append(product_name)
#             # time.sleep(1)

        

#         product_brandname = ""
#         while len(product_brandname) == 0:
#             # print("브랜드 가지러들어옴")
#             try:
#                 product_brandname = browser.find_element_by_class_name("prod-brand-name").text
#             except:
#                 product_brandname = ""
#             # print(product_brandname)
#             templist.append(product_brandname)
#             # time.sleep(1)

#             errorcnt += 1
#             if errorcnt > 3:
#                 errorbreak = 1
#                 del templist[-1]
#                 del templist[-1]
#                 del templist[-1]
#                 del templist[-1]
#                 break
#         if errorbreak == 1:
#             errorbreak =0
#             errorcnt =0
            
#             # 브랜드 빈칸    
#             templist.append("")
#             # continue
#         elif errorbreak == 0:
#             errorcnt =0
        
#         # 타입 빈칸    
#         templist.append("")

#         product_option2 = ""
#         while len(product_option2) == 0:
#             # print("옵션가지러 들어옴")
#             try:
#                 # print("try")
#                 product_option = browser.find_element_by_class_name("prod-option  ")
#                 # print("여긴했음1")
#                 product_option2 = product_option.find_element_by_class_name("value").text
#                 # print("여긴했음2")
#                 if len(product_option2) == 0:
#                     # print("if 도는중")
#                     break
#             except:
#                 # print("except")
#                 product_option2 = ""
#                 break
        
#             # print(product_option2)
#             # time.sleep(1)
        

#         product_option2 = product_option2.replace("입","")
#         product_option2 = product_option2.replace("매","")
#         product_option2 = product_option2.replace("병","")
#         product_option2 = product_option2.replace("세트","")
#         product_option2 = product_option2.replace("set","")
#         product_option2 = product_option2.replace("ml","")
#         product_option2 = product_option2.replace("팩","")
#         product_option2 = product_option2.replace("박스","")
#         product_option2_mod = product_option2.replace("개","")
#         # print(product_option2_mod)
#         product_option2_mod2 = product_option2_mod.replace("g","")
#         # print(product_option2_mod2)
        
#         product_option2_mod2_split = product_option2_mod2.split(" × ")
#         # print(product_option2_mod2_split)

#         if len(product_option2_mod2_split) == 2:
#             if 'k' in product_option2_mod2_split[0]:
#                 try:
#                     temp1 = float(product_option2_mod2_split[0].replace('k',""))*1000
#                 except:
#                     temp1 = product_option2_mod2_split[0]
#             else:
#                 try:
#                     temp1 = float(product_option2_mod2_split[0])
#                 except:
#                     temp1 = product_option2_mod2_split[0]
#             try:
#                 temp2 = float(product_option2_mod2_split[1])
#             except:
#                 temp2 = product_option2_mod2_split[1]
#         else:
#             temp1 = ""
#             temp2 = product_option2_mod2_split[0]

#         print(temp1, temp2)
#         templist.append(temp1)
#         templist.append(temp2)

#         # 총용량 빈칸    
#         templist.append("")
        
        
#         # 대용량 빈칸    
#         templist.append("")
            

#         product_price = ""
#         while len(product_price) == 0:
#             print("가격가지러 들어옴")
#             try:
#                 product_price = browser.find_element_by_class_name("total-price").text
#             except:
#                 product_price = ""

#             errorcnt += 1
#             if errorcnt > 3:
#                 errorbreak = 1
#                 break
#         if errorbreak == 1:
#             errorbreak =0
#             errorcnt =0
#             continue
#         elif errorbreak == 0:
#             errorcnt =0

#         print(product_price)
#         product_price_mod = product_price.replace("원","")
#         product_price_mod2 = product_price_mod.replace(",","")
#         templist.append(product_price_mod2)
        
        
# # result = re.findall('\d+', d)[0]
# # print(result)
#         try:
#             product_delivery = browser.find_element_by_class_name("prod-shipping-fee-container")
#             if '그 외' in product_delivery.text:
#                 print("조건부 무료배송")
#                 textlocation = product_delivery.text.find('그 외')
#                 print(textlocation)
#                 textlocation = product_delivery.text[35:]
#                 print(textlocation)
#                 product_delivery_mod = textlocation.replace("원","")
#                 product_delivery_mod2 = product_delivery_mod.replace("배송비 ","")
#                 product_delivery_mod3 = product_delivery_mod2.replace(",","")
#                 product_delivery_mod3 = re.findall('\d+', product_delivery_mod3)[0] # 숫자만 가져오기
#                 templist.append(product_delivery_mod3)
                
#             elif '착불' in product_delivery.text:
#                 print("착불")
#                 templist.append('착불')
#             elif '무료배송' in product_delivery.text:
#                 print("무료배송")
#                 templist.append(0)
#             else:
#                 print(product_delivery.text)
#                 product_delivery_mod = product_delivery.text.replace("원","")
#                 product_delivery_mod2 = product_delivery_mod.replace("배송비 ","")
#                 product_delivery_mod3 = product_delivery_mod2.replace(",","")
#                 product_delivery_mod3 = re.findall('\d+', product_delivery_mod3)[0] # 숫자만 가져오기
#                 templist.append(product_delivery_mod3)
#         except:
#             print("배송정보 없음")
#             templist.append('배송정보 없음')
            

        
#         # 합계금액 빈칸    
#         templist.append("")
            
        
#         # 단가 빈칸    
#         templist.append("")
            
#         try:
#             product_gume = browser.find_element_by_class_name("prod-buy-header__productreview")
#             print(product_gume.text)
#             product_gume_mod2 = product_gume.text.replace(",","")
#             product_gume_mod3 = product_gume_mod2.replace("개 상품평","")
#             templist.append(product_gume_mod3)
#         except:
#             print("상품평 없음")
#             templist.append(0)

        
#         # url    
#         templist.append(product)
            
#         if len(templist) !=13:
#             print(len(templist))
#             print(templist)
#         print("")
#         csvlist.append(templist)

#         # df = pd.DataFrame(csvlist,columns=['상품명','브랜드','타입','단위','개수','총용량','대용량,'가격','배송비','합계금액','단가','리뷰수','url'])
#         # df.to_csv('coupang_product.csv', index=False, encoding='cp949')

#     print(csvlist)
#     filename = 'coupang_product_'+keyword+'.csv'
#     df = pd.DataFrame(csvlist,columns=['상품명','브랜드','타입','단위','개수','총용량','대용량','가격','배송비','합계금액','단가','리뷰수','url'])
#     df.to_csv(filename, index=False, encoding='utf-8-sig')
#     # df.to_csv('coupang_product.csv', index=False, encoding='cp949')


