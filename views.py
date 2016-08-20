from django.shortcuts import render, redirect, HttpResponse
#from models import Users

# Create your views here.
def index(request):
    return render(request,'login_reg/index.html')

def register(request):
    return redirect('/')

def login(request):
    return redirect('/')
