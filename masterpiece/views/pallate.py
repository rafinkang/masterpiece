import base64
import datetime
import os
from io import BytesIO

import cv2
import joblib
import numpy as np
import pandas as pd
from colorutils.convert import hsv_to_hex
from django.core.files.base import ContentFile
from django.http import HttpResponse
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from masterpiece.classes.CycleganLoadWeight import CycleganLoadWeight
from masterpiece.classes.Spuit import Spuit
from PIL import Image
from masterpiece.models.GallaryList import GallaryList


def pallate(request):
    return render(request, 'pallate/pallate.html')

# ch_style
def temp_img_upload(request):
    dataURI = request.POST.dict()['dataURI']
    user_idx = request.POST.dict()['userIDX']
    temp_img_path = 'masterpiece/static/upload_images/temp_images/'

    filename = user_idx + '_' + datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + '.jpg'
    path = temp_img_path + '/' + filename

    imgdata = base64_decode(dataURI)

    with open(path, 'wb') as f:
        f.write(imgdata)

    return HttpResponse(filename)

def change_masterpiece(request):
    img_name = request.POST.dict()['img_name']
    temp_img_full_path = 'masterpiece/static/upload_images/temp_images/' + img_name

    clw = CycleganLoadWeight()
    return HttpResponse(clw.change_style(temp_img_full_path, img_name))

def download_img(request):
    # 임시 저장 이미지 중 찾을 이미지 2개
    user_idx = request.POST.dict()['userIDX']
    masterpiece_img_name = request.POST.dict()['masterpieceImageName'] # 명화화 한 임시 저장 이미지 이름
    img_name = masterpiece_img_name.replace('_masterpiece', '') # 명화화 하기 전 임시 저장 이미지 이름
    
    original_img_path = 'masterpiece/static/upload_images/original_images/'
    masterpiece_img_path = 'masterpiece/static/upload_images/masterpiece_images/'
    temp_img_path = 'masterpiece/static/upload_images/temp_images/'

    # 원본 이미지 서버 저장
    img = Image.open(temp_img_path + img_name)
    img.save(original_img_path + img_name)

    # 명화화 이미지 서버 저장
    master_img = Image.open(temp_img_path + masterpiece_img_name)
    master_img.save(masterpiece_img_path + masterpiece_img_name)

    # DB저장
    sql = "insert into gallary_list(user_idx, image_name, image_url, image_type) values(%s, %s, %s);"
    data = [[user_idx, img_name, original_img_path + img_name], [user_idx, masterpiece_img_name, masterpiece_img_path + masterpiece_img_name]]
    GallaryList.executemany(sql, data)

    # 임시저장 이미지 삭제
    os.remove(img_name + temp_img_path)
    os.remove(temp_img_path + masterpiece_img_name)

    return HttpResponse(masterpiece_img_path + masterpiece_img_name)

# color_pick
def color_pick(request):
    request_dict = request.POST.dict()
    img = base64_to_cv2(request_dict['dataURI'])

    image = Spuit(image=img)
    hsv = image.get_hsv360()
    percent = image.get_percent()

    pallate_list = np.array(hsv).reshape(1,12)
    pallate_dp =  pd.DataFrame(pallate_list, columns=['h1','s1','v1','h2','s2','v2','h3','s3','v3','h4','s4','v4'])
    pallate_x = pallate_dp[['h1','s1','v1','h2','s2','v2','h3','s3','v3','h4','s4','v4']]
    color_x = pallate_dp[['h1']]
    
    
    # 컬러 모델 로드
    color_model = joblib.load("masterpiece/joblib/color_forest.joblib")
    # 콘트라스트 파스텔 모델 로드
    cp_model = joblib.load("masterpiece/joblib/cp_forest.joblib")
    # 쿨웜 모델 로드
    cw_model = joblib.load("masterpiece/joblib/cw_forest.joblib")
    # 시즌 모델 로드
    season_model = joblib.load("masterpiece/joblib/seasons_forest.joblib")
    # 명암 모델 로드
    value_model = joblib.load("masterpiece/joblib/value_forest.joblib")

    # 모델 실행
    color_pred = color_model.predict(color_x)
    cp_pred = cp_model.predict(pallate_x)
    cw_pred = cw_model.predict(pallate_x)
    season_pred = season_model.predict(pallate_x)
    value_pred = value_model.predict(pallate_x)
    
    pallate = pallate_list[0]
    hex1 = hsv_to_hex((pallate[0],pallate[1]/100,pallate[2]/100))
    hex2 = hsv_to_hex((pallate[3],pallate[4]/100,pallate[5]/100))
    hex3 = hsv_to_hex((pallate[6],pallate[7]/100,pallate[8]/100))
    hex4 = hsv_to_hex((pallate[9],pallate[10]/100,pallate[11]/100))
    
    result = {
        'h1'    : str(pallate[0]),
        's1'    : str(pallate[1]),
        'v1'    : str(pallate[2]),
        'h2'    : str(pallate[3]),
        's2'    : str(pallate[4]),
        'v2'    : str(pallate[5]),
        'h3'    : str(pallate[6]),
        's3'    : str(pallate[7]),
        'v3'    : str(pallate[8]),
        'h4'    : str(pallate[9]),
        's4'    : str(pallate[10]),
        'v4'    : str(pallate[11]),
        "percent1" : str(round(percent[0]*100, 1)),
        "percent2" : str(round(percent[1]*100, 1)),
        "percent3" : str(round(percent[2]*100, 1)),
        "percent4" : str(round(percent[3]*100, 1)),
        "hex1"  : str(hex1),
        "hex2"  : str(hex2),
        "hex3"  : str(hex3),
        "hex4"  : str(hex4),
        "color_pred" : str(color_pred[0]),
        "cp_pred" : str(cp_pred[0]),
        "cw_pred" : str(cw_pred[0]),
        "season_pred" : str(season_pred[0]),
        "value_pred" : str(value_pred[0])
    }
    return JsonResponse(result)

def base64_decode(base64_str):
    img_str = base64_str.split(';base64,')[1]
    imgdata = base64.b64decode(img_str)
    return imgdata

def base64_to_image(base64_str):
    img_str = base64_str.split(';base64,')[1]
    return Image.open(BytesIO(base64.b64decode(img_str)))

def base64_to_cv2(base64_str):
    img_str = base64_str.split(';base64,')[1]
    im_bytes = base64.b64decode(img_str)
    im_arr = np.frombuffer(im_bytes, dtype=np.uint8)  # im_arr is one-dim Numpy array
    img = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)
    return img
