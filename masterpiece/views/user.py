from django.shortcuts import render, redirect
from django.http import HttpResponse
from masterpiece.models.User import User
from django.http.response import JsonResponse
from django.contrib.auth import logout as auth_logout


# Create your views here.
# 컨트롤러 역할 비즈니스 로직 구현

# 로그인 페이지 이동
def login(request):
    return render(request, 'user/user_login.html')

# 회원가입 페이지 이동
def register(request):
    return render(request, 'user/user_register.html')

# 비밀번호 찾기 페이지 이동 
def findpw(request):
    return render(request, 'user/user_findpw.html')

# 비밀번호 변경 페이지 이동 
def modifypw(request):
    return render(request, 'user/user_modifypw.html')

# 로그아웃 후 로그인 페이지 
def logout_go(request):
    return render(request, 'user/user_logout.html')

# 아이디 중복 체크 
def idcheck(request):
    req = request.POST.dict()
    user = User()
    result = user.idcheck(req['user_id'])
    
    if result == None:
        return HttpResponse("1")
    else:
        return HttpResponse("0")


    
# 회원가입, db입력
def insert_user(request):
    req = request.POST.dict()
    user = User()
    result = user.insert_user(req['user_id'],req['password'],req['user_name'],req['sex'],req['birth'],req['job'],req['company'] )

    if result == None:
        return HttpResponse("0")
    else:
        return HttpResponse("1")


#로그인 
def login_go(request):
    req = request.POST.dict()
    user = User()
    result = user.login_go(req['user_id'],req['password'])

    if result == None:
        return HttpResponse("0")
    else:
        request.session['user_idx'] = str(result[0]["user_idx"])
        request.session['user_id'] = str(result[0]["user_id"])
        # request.session['password'] = str(result[0]["password"])
        request.session['user_name'] = str(result[0]["user_name"])
        request.session['sex'] = str(result[0]["sex"])
        request.session['birth'] = str(result[0]["birth"])
        request.session['job'] = str(result[0]["job"])
        request.session['company'] = str(result[0]["company"])
        return JsonResponse(result[0])

    #로그아웃 
def logout(request):
    auth_logout(request)
    request.session.flush()
    return HttpResponse("1");

#비밀번호 찾기 비교 
def findpw_search(request):
    req = request.POST.dict()
    user = User()
    result = user.findpw(req['user_id'],req['user_name'])    
    if result == None:
        return HttpResponse("1")
    else:
        return HttpResponse("0")

#비밀번호 변경 
def modifypw_go(request):
    req = request.POST.dict()
    user = User()
    result = user.modifypw_go(req['password'],req['user_id'],req['user_name'])
    
    if result == None:
        return HttpResponse("1")
    else:
        return HttpResponse("0")
