from django.shortcuts import render, redirect
from masterpiece.models import *
from masterpiece.example_class.forms import post_frm
from masterpiece.example_class.DbConn import *

# Create your views here.

def index(request):
    return render(request, 'index.html')

# 단순 페이지 이동
def normal_res(request):
    return render(request, 'masterpiece/normal_res.html')

# GET방식
def get_res(request):
    return  render(request, 'masterpiece/get_res.html', context=request.GET.dict()) # context=request.GET.dict() : reqeust의 get으로 받은 parameter를 dictionary형태로 넘김

# POST방식
def post_res(request):
    if request.method == 'POST': # form 생성 후 POST요청시 사용자가 입력한 값 처리
        form = post_frm(request.POST) # form정보 가져오기

        if form.is_valid(): # 유효성 검사
            form.save(request.POST.dict()) # DB저장 (insert)
        return render(request, 'masterpiece/post_res.html', context=request.POST.dict()) # 결과화면으로 이동
    else: # form 생성하기, create_post_frm.html에서 submit할 때 해당 post_res function을 다시 call
        form = post_frm()
    
    return render(request, 'masterpiece/create_post_frm.html', {'form': form})

# DB select
def select_res(request):
    db = DbConn()
    sql = 'select * from color_pallete limit 200'
    test_list = db.select(sql) # return type : dictionary

    return render(request, 'masterpiece/select_res.html', {'test_list': test_list})

# DB update
def update_res(request): # 원래 GET으로 하면 안됨, POST로 바꿔야함
    up_dict = request.GET.dict()
    db = DbConn()
    test2 = up_dict['data2']
    test3 = up_dict['data3']
    test = up_dict['data1']
    
    sql = f'update test set test2 = {test2}, test3 = {test3} where test = {test}'

    db.execute(sql)

    return redirect('/select_res')

# DB delete
def delete_res(request): # 원래 GET으로 하면 안됨, POST로 바꿔야함
    del_dict = request.GET.dict()
    db = DbConn()
    
    sql = 'delete from test where test = %s and test2 = %s and test3 = %s'
    data = [del_dict['data1'], del_dict['data2'], del_dict['data3']]

    db.execute(sql, data)

    return redirect('/select_res')
