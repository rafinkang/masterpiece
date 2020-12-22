from django.shortcuts import render, redirect
from django.http import HttpResponse
from masterpiece.classes.CycleganLoadWeight import CycleganLoadWeight
from django.core.files.base import ContentFile
import datetime

def ch_style(request):
    return render(request, 'pallate/ch_style.html')

def temp_img_upload(request):
    req = request.POST.dict()

    img_f = req['img_f']
    original_name = req['original_name']
    img_extension = req['img_extension']
    temp_img_path = 'C:/Users/jypar/finalproject/masterpiece/temp_img'

    filename = filename + '-' + datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + img_extension
    path = temp_img_path + '/' + filename

    destination = open(path, 'wb+')

    for chunk in img_f.chunks():
        destination.write(chunk)
    destination.close()

    return path

def change_masterpiece(request):
    dataURI = request.POST.dict()['dataURI']

    # get file from json data
    format_image, img_str = dataURI.split(';base64,')
    # file content
    file_content = ContentFile(base64.b64decode(img_str))

    print('img_str ::::::::::::::', img_str)
    print('file_content :::::::::::::', file_content)

    clw = CycleganLoadWeight()
    clw.change_style(file_content)

    # print("f_path ::::::::::::::: ", f_path)
    return HttpResponse("0")
