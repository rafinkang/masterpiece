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

    
# 회원가입, db입력
def insert_user(request):
    req = request.POST.dict()
    user = User()
    result = user.insert_user(req['user_id'],req['password'],req['user_name'],req['sex'],req['birth'],req['job'],req['company'] )

    if result == None:
        print(result,"회원가입 못했다!!!!!!!")
        return HttpResponse("0")
    else:
        print(result,"회원가입했다!!!!!!!")
        return HttpResponse("1")
    # return True or False

#로그인 
def login_go(request):
    req = request.POST.dict()
    user = User()
    result = user.login_go(req['user_id'],req['password'])

    if result == None:
        print(result,"로그인 실패")

        
        return HttpResponse("0")
    else:
        print(result,"로그인 성공")
        
        print(result[0],"딕셔너리로나와라")
        print(result[0]['user_idx'],"유저 인덱스")

        # request.session['aa'] = 'aa11111'

        # print(request.session.get('aa'))
        # request.session['user'] = 'result[0]["user_id"]'
        # print(request.session.get('user'))
        return HttpResponse("1")

    
