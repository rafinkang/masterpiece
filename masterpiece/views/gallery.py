from django.shortcuts import render, redirect
from masterpiece.models import *
from masterpiece.example_class.forms import post_frm
from masterpiece.example_class.DbConn import *
from masterpiece.models.GallaryList import GallaryList
from django.http import HttpResponse
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
    return render(request, 'gallery/image_gallery/image_list.html')

# 이미지 검색
def image_filter(request):
    request_dict = request.POST.dict()    
    gl = GallaryList()

    res = gl.image_filter(request_dict['opt_type'], request.session.get('user_idx'))

    return render(request, 'gallery/image_gallery/image_content.html', {
        'res': res
    })

# 좋아요 클릭
def image_like(request) :
    gl_idx = request.POST.dict()['gl_idx']
    gl = GallaryList()
    res = -1

    if request.session.get('user_idx'): # 세션에 유저 정보가 있는 경우만

        user_like_list = gl.get_user_like(gl_idx, request.session.get('user_idx'))

        if user_like_list != None : # 해당 이미지는 사용자가 이미 좋아요 누름 -> 좋아요 취소
            gl.drop_like(gl_idx, request.session.get('user_idx'))
            res = 1
        else: # 해당 이미지 사용자 좋아요 없음 -> 좋아요 등록
            gl.set_like(gl_idx, request.session.get('user_idx'))
            res = 0

    return HttpResponse(res)
