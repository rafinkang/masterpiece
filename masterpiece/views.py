from django.shortcuts import render, redirect
from masterpiece.models import *
from masterpiece.example_class.forms import post_frm
from masterpiece.example_class.DbConn import *

# Create your views here.

def index(request):
    return render(request, 'index.html')

def normal_res(request):
    return render(request, 'masterpiece/normal_res.html')

def get_res(request):
    return  render(request, 'masterpiece/get_res.html', context=request.GET.dict())

def post_res(request):
    if request.method == 'POST': # 사용자가 입력한 값 처리
        form = post_frm(request.POST)

        if form.is_valid():
            form.save(request.POST.dict()) # DB저장 (insert)
        return render(request, 'masterpiece/post_res.html', context=request.POST.dict())
    else: # form 보여주기, create_post_frm.html에서 submit할 때 해당 function을 다시 call
        form = post_frm()
    
    return render(request, 'masterpiece/create_post_frm.html', {'form': form})

def select_res(request):
    db = DbConn()
    sql = 'select * from test limit 5'
    test_list = db.select(sql)

    return render(request, 'masterpiece/select_res.html', {'test_list': test_list})

def delete_res(request):
    del_dict = request.GET.dict()
    db = DbConn()
    
    sql = 'delete from test where test = %s and test2 = %s and test3 = %s'
    data = [del_dict['post_message1'], del_dict['post_message2'], del_dict['post_message3']]
    
    db.execute(sql, data)

    return redirect('/select_res') 
