from django.shortcuts import render, redirect
from masterpiece.models import *
from masterpiece.example_class.forms import post_frm
from masterpiece.example_class.DbConn import *

# Create your views here.

# 색상 입히기 페이지 이동
def color_dress(request):
    return render(request, 'color_dress/color_dress.html')
