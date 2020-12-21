from django.shortcuts import render, redirect
from django.http import HttpResponse
from masterpiece.models.User import User

# Create your views here.
# 컨트롤러 역할 비즈니스 로직 구현

# 로그인 페이지 이동
def login(request):
    return render(request, 'user/user_login.html')

# 회원가입 페이지 이동
def register(request):
    return render(request, 'user/user_register.html')

# 아이디 중복 체크 
def idcheck(request):
    req = request.POST.dict()
    user = User()
    result = user.idcheck(req['user_id'])
    
    if result == None:
        print(result,"참이다!!!!!!!")
        return HttpResponse("1")
    else:
        print(result,"거짓이다!!!!!!!")
        return HttpResponse("0")
    # return True or False

def insert_user(request):
    req = request.POST.dict()
    user = User()
    result = user.insert_user(req['user_id','password', 'user_name', 'sex', 'birth', 'job','company'])

    if result == None:
        print(result,"회원가입!!!!!!!")
        return HttpResponse("1")
    else:
        print(result,"회원가입실패!!!!!!!")
        return HttpResponse("0")