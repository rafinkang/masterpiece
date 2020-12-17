from django.shortcuts import render, redirect
from masterpiece.models import *

from masterpiece.example_class.DbConn import *

def index(request):
    return render(request, 'pallate/pallate.html')

def colorpick(request):
    return render(request, 'pallate/colorpick.html')

def ch_style(request):
    return render(request, 'pallate/ch_style.html')
    
# 색상 입히기 페이지 이동
def color_dress(request):
    return render(request, 'pallate/color_dress.html')
