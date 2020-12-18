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
        return HttpResponse("0")
    else:
        return HttpResponse("1")
    
    # return True or False