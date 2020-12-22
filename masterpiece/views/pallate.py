from django.shortcuts import render, redirect

def pallate(request):
    return render(request, 'pallate/pallate.html')

