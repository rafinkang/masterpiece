from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.http import HttpResponse
from masterpiece.classes.CycleganLoadWeight import CycleganLoadWeight
from django.core.files.base import ContentFile
import datetime
import base64
from PIL import Image
from io import BytesIO
import numpy as np
import cv2
from masterpiece.classes.Spuit import Spuit

def pallate(request):
    return render(request, 'pallate/pallate.html')

# ch_style
def temp_img_upload(request):
    dataURI = request.POST.dict()['dataURI']
    temp_img_path = 'masterpiece/images/tmp'

    filename = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + '.jpg'
    path = temp_img_path + '/' + filename

    img_str = dataURI.split(';base64,')[1]
    imgdata = base64.b64decode(img_str)

    with open(path, 'wb') as f:
        f.write(imgdata)

    return HttpResponse("0")

def change_masterpiece(request):
    # clw = CycleganLoadWeight()
    # clw.change_style(file_content)

    return 'ok'

# color_pick
def color_pick(request):
    request_dict = request.POST.dict()
    dataURI = request_dict['dataURI']
    img = base64_to_cv2(dataURI)
    print(img)
    image = Spuit(image=img)
    hsv = image.get_hsv360()
    print(hsv)
    
    return HttpResponse('hihi')

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