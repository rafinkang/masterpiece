from django.shortcuts import render, redirect
from django.http import HttpResponse
from masterpiece.classes.CycleganLoadWeight import CycleganLoadWeight
from django.core.files.base import ContentFile
import datetime
import base64

def ch_style(request):
    return render(request, 'pallate/ch_style.html')

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
