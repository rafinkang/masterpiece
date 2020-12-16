from django.shortcuts import render, redirect
from masterpiece.models import *

from masterpiece.example_class.DbConn import *

def index(request):
    return render(request, 'pallate/pallate.html')

def colorpick(request):
    return render(request, 'pallate/colorpick.html')

def ch_style(request):
    return render(request, 'pallate/ch_style.html')