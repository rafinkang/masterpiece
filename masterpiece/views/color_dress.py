from django.shortcuts import render, redirect

# 색상 입히기 페이지 이동
def color_dress(request):
    return render(request, 'pallate/color_dress.html')
