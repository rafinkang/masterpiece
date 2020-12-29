from django.shortcuts import render, redirect
from masterpiece.models import *
from masterpiece.example_class.forms import post_frm
from masterpiece.example_class.DbConn import *
from masterpiece.models.GallaryList import GallaryList
from masterpiece.models.ColorList import ColorList

# Create your views here.

# 색상갤러리 페이지 이동
def color_gallery(request):
    cl = ColorList()
    res = cl.list_filter()
    return render(request, 'gallery/color_gallery/color_gallery.html',{
        'res': res
    })

def color_list(request):
    request_dict = request.POST.dict()    
    cl = ColorList()
    res = cl.list_filter(request_dict['color_type'], request_dict['season_type'], request_dict['cw_type'], request_dict['cp_type'], request_dict['value_type'])
    return render(request, 'gallery/color_gallery/color_list.html',{
        'res': res
    })

# 색상갤러리 디테일 페이지 이동
def color_gallery_detail(request):
    return render(request, 'gallery/color_gallery/color_gallery_detail.html')

# 이미지 리스트 이동
def image_list(request):
    return render(request, 'gallery/imageGallery/image_list.html')

# 이미지 검색
def image_filter(request):
    request_dict = request.POST.dict()
    gl = GallaryList()
    res = gl.select_all()

    return render(request, 'gallery/imageGallery/image_content.html', {
        'res': res
    })

    request_dict = request.POST.dict()    
    gl = GallaryList()
    res = gl.emotion_filter(request_dict['artist_type'], request_dict['style_type'])

    return render(request, 'gallery/imageGallery/image_content.html', {
        'res': res
    })
