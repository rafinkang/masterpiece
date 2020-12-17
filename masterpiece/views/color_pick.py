from django.shortcuts import render, redirect

def color_pick(request):
    return render(request, 'pallate/color_pick.html')

