from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
from .models import *


def index(request):
    return render(request, 'coaching_app/login_reg.html')


def user(request):
    # User processor
    errors = User.objects.validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags="register")
        return redirect('/#toregister')
    else:
        username = request.POST["username"]
        email = request.POST["email"]
        matched_user = User.objects.filter(username=request.POST["username"])
        if len(matched_user) > 0:
            messages.error(request, 'Username unavailable', extra_tags="register")
            return redirect('/#toregister')
        pw_hash = bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt())
        new_user = User.objects.create(
            username=username, email=email, password=pw_hash)
        request.session["new_user_id"] = new_user.id  
    return redirect('/registration')


def registration(request):
    context = {
        "reg_user": User.objects.get(id = request.session["new_user_id"]),
    }
    return render(request, 'coaching_app/success.html', context)


def login_process(request):
    matched_user = User.objects.filter(username=request.POST['username'])
    print(matched_user)
    if len(matched_user) < 1:
        messages.error(request, 'Email or password does not match', extra_tags="login")
        return redirect('/')
    if bcrypt.checkpw(request.POST['password'].encode(), matched_user[0].password.encode()):
        request.session['username'] = request.POST['username']
        request.session['username'] = request.POST['username']
        return redirect('/login')
    else:
        messages.error(request, 'Email or password do not match', extra_tags="login")
        return redirect('/')
    return redirect('/')


def login(request):
    context = {
        "reg_user": User.objects.filter(username = request.session["username"])[0]
    }
    return render(request, 'coaching_app/success.html', context)

def logout(request):
    request.session.clear()
    return redirect('/')

