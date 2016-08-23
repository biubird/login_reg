from django.shortcuts import render, redirect, HttpResponse
from models import User
from django.contrib import messages
from django.core.urlresolvers import reverse

# Create your views here.
def index(request):
    return render(request,'login_reg/index.html')

def register(request):
    if request.method == "POST":
        print "hello"
        result = User.userMgr.register(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=request.POST['password'], password_conf=request.POST['password_conf'])
        print result
        if result[0]:
            request.session['user'] = result[1].first_name
            return redirect(reverse('_success'))
        else:
            for error in result[1]:
                messages.add_message(request, messages.INFO, result[1][error])
            return redirect(reverse('_index'))
    else:
        messages.add_messages(request, messages.INFO, 'Please Try Again')
        return redirect(reverse('_index'))

def login(request):
    if request.method == 'POST':
        print 'hello again'
        result = User.userMgr.login(email=request.POST['email'], password=request.POST['password'])
        if result[0]:
            request.session['user'] = result[1].first_name
            return redirect(reverse('_success'))
        else:
            for error in result[1]:
                messages.add_messages(request, messages.INFO, result[1][error])
                return redirect(reverse('_index'))
    else:
        messages.add_messages(request, messages.INFO, 'Please Try Again')
        return redirect(reverse('_index'))

def success(request):
    context = {
        'first_name': request.session['user']
    }
    return render(request, 'login_reg/success.html', context)

def logout(request):
    return redirect('/')
