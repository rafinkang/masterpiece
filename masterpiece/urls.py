# 서브앱 urls
from django.contrib import admin
from django.urls import path, include
from .views import main, pallate, ch_style, user, gallery

urlpatterns = [
    path('', main.index, name='main'),
    path('main', main.index, name='main'),

    path('login', user.login, name='login'),
    path('login/login_go', user.login_go, name='login/login_go'),

    path('register', user.register, name='register'),
    path('register/idcheck', user.idcheck, name='register/idcheck'),
    path('register/insert_user', user.insert_user, name='register/insert_user'),
    

    
    # pallate 
    path('pallate', pallate.pallate, name='pallate'),

    # ch_style(change_style)
    path('pallate/ch_style/change_masterpiece', ch_style.change_masterpiece, name='ch_style/change_masterpiece'),
    path('pallate/ch_style/temp_img_upload', ch_style.temp_img_upload, name='ch_style/temp_img_upload'),
    
    # gallery
    path('gallery/color_gallery', gallery.color_gallery, name='color_gallery'),
    path('gallery/color_gallery_detail', gallery.color_gallery_detail, name='color_gallery_detail'),

    ######################################## example ########################################

    path('example_index', main.example_index, name='example_index'),

    path('normal_res', main.normal_res, name='normal_res'), # 단순 페이지 이동

    path('get_res/<str:get_message1>/<str:get_message2>', main.get_res, name='get_res'), # url + parameter 페이지 이동
    path('get_res', main.get_res, name='get_res'), # form action = 'GET'
    path('post_res', main.post_res, name='post_res'), # form action = 'POST'

    path('select_res', main.select_res, name='select_res'), # DB select
    path('update_res', main.update_res, name='update_res'), # DB update
    path('delete_res', main.delete_res, name='delete_res') # DB delete
]
