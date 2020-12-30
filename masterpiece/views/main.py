from django.shortcuts import render, redirect
from masterpiece.models import *

# Create your views here.

# 메인 페이지 이동
def index(request):
    return render(request, 'main.html')