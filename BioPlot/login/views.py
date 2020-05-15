import hashlib
from django.shortcuts import render,redirect
from . import models
from .forms import UserForm,RegisterForm

# Create your views here.

def hash_code(s, hk='lxf'):
    h = hashlib.sha256()
    s += hk
    h.update(s.encode())
    return h.hexdigest()

def login(request):
    if request.session.get('is_login',None):
        return redirect('/index')
    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = "please check in the content！"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = models.User.objects.get(name=username)
                if user.password == hash_code(password):
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    return redirect('/index/')
                else:
                    message = "uncorrect passwd！"
            except:
                message = "uncorrect user！"
        return render(request, 'login/login.html', locals())
    login_form = UserForm()
    return render(request,'login/login.html', locals())

def index(request):
    pass
    return render(request,'login/index.html')

def register(request):
    if request.session.get('is_login', None):
        return redirect("/index/")
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        message = "please check in the content！"
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            sex = register_form.cleaned_data['sex']
            if password1 != password2:
                message = "Enter the password twice is different!"
                return render(request, 'login/register.html', locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:
                    message = "User already exists, please re-select username"
                    return render(request, 'login/register.html', locals())
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user: 
                    message = "The email address has been registered, please use another email address"
                    return render(request, 'login/register.html', locals())
                new_user = models.User.objects.create()
                new_user.name = username
                new_user.password = hash_code(password1)
                new_user.email = email
                new_user.sex = sex
                new_user.save()
                return redirect('/login/')
    register_form = RegisterForm()
    return render(request,'login/register.html', locals())

def logout(request):
    if not request.session.get('is_login', None):
        return redirect("/index/")
    request.session.flush()
    return redirect('/index/')

def contact(request):
    pass
    return render(request,'login/contact.html', locals())
