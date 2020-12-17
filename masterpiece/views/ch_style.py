from django.shortcuts import render, redirect


def ch_style(request):
    return render(request, 'pallate/ch_style.html')
    
