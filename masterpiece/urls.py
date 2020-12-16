# 서브앱 urls

from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='main'),
    path('main/', views.index, name='main'),

    path('ch-style/', views.ch_style, name='ch_style'),

    ######################################## example ########################################

    path('example_index/', views.example_index, name='example_index'),

    path('normal_res/', views.normal_res, name='normal_res'), # 단순 페이지 이동

    path('get_res/<str:get_message1>/<str:get_message2>', views.get_res, name='get_res'), # url + parameter 페이지 이동
    path('get_res/', views.get_res, name='get_res'), # form action = 'GET'
    path('post_res/', views.post_res, name='post_res'), # form action = 'POST'

    path('select_res/', views.select_res, name='select_res'), # DB select
    path('update_res/', views.update_res, name='update_res'), # DB update
    path('delete_res/', views.delete_res, name='delete_res') # DB delete
]
