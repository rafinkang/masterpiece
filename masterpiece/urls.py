# 서브앱 urls

from django.contrib import admin
from django.urls import path, include
from .views import main, pallate, user, gallery

urlpatterns = [
    path('', main.index, name='main'),
    path('main/', main.index, name='main'),

    path('login/', user.login, name='login'),
    path('register/', user.register, name='register'),

    
    # pallate 
    path('pallate/', pallate.index, name='pallate'),
    path('pallate/colorpick/', pallate.colorpick, name='colorpick'),
    path('pallate/ch-style/', pallate.ch_style, name='ch_style'),

    # gallery
    path('gallery/color_gallery/', gallery.color_gallery, name='color_gallery'),
    path('gallery/color_gallery_detail/', gallery.color_gallery_detail, name='color_gallery_detail'),

    ######################################## example ########################################

    path('example_index/', main.example_index, name='example_index'),

    path('normal_res/', main.normal_res, name='normal_res'), # 단순 페이지 이동

    path('get_res/<str:get_message1>/<str:get_message2>', main.get_res, name='get_res'), # url + parameter 페이지 이동
    path('get_res/', main.get_res, name='get_res'), # form action = 'GET'
    path('post_res/', main.post_res, name='post_res'), # form action = 'POST'

    path('select_res/', main.select_res, name='select_res'), # DB select
    path('update_res/', main.update_res, name='update_res'), # DB update
    path('delete_res/', main.delete_res, name='delete_res') # DB delete
]
