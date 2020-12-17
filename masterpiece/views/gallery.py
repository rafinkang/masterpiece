from django.shortcuts import render, redirect
from masterpiece.models import *
from masterpiece.example_class.forms import post_frm
from masterpiece.example_class.DbConn import *

# Create your views here.

# 색상갤러리 페이지 이동
def color_gallery(request):
    return render(request, 'gallery/color_gallery.html')

# 색상갤러리 디테일 페이지 이동
def color_gallery_detail(request):
    return render(request, 'gallery/color_gallery_detail.html')
