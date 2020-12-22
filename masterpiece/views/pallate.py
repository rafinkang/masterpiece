from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.http import HttpResponse
from masterpiece.classes.CycleganLoadWeight import CycleganLoadWeight
from django.core.files.base import ContentFile
import datetime
import base64
from PIL import Image
from io import BytesIO

def pallate(request):
    return render(request, 'pallate/pallate.html')

# ch_style
def temp_img_upload(request):
    dataURI = request.POST.dict()['dataURI']
    temp_img_path = 'masterpiece/images/tmp'

    filename = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + '.jpg'
    path = temp_img_path + '/' + filename

    imgdata = base64_decode(dataURI)

    with open(path, 'wb') as f:
        f.write(imgdata)

    return HttpResponse(filename)

def change_masterpiece(request):
    img_name = request.POST.dict()['img_name']
    img_path = 'masterpiece/images/tmp/' + img_name

    clw = CycleganLoadWeight()
    return HttpResponse(clw.change_style(img_path, img_name))

# color_pick
def color_pick(request):
    request_dict = request.POST.dict()
    dataURI = request_dict['dataURI']
    img = base64_to_image(dataURI)
    print(img)
    
    
    return HttpResponse('hihi')

def base64_decode(base64_str):
    img_str = base64_str.split(';base64,')[1]
    imgdata = base64.b64decode(img_str)
    return imgdata

def base64_to_image(base64_str):
    img_str = base64_str.split(';base64,')[1]
    return Image.open(BytesIO(base64.b64decode(img_str)))