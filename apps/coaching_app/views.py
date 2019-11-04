from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
from .models import *


def home_page(request):
    return render(request, 'coaching_app/index.html')


def login_page(request):
    return render(request, 'coaching_app/login_reg.html')


def user_process(request):
    errors = User.objects.validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags="register")
        return redirect('/login_page#toregister')
    else:
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST["username"]
        email = request.POST["email"]
        matched_user = User.objects.filter(username=request.POST["username"])
        if len(matched_user) > 0:
            messages.error(request, 'Username unavailable',
                           extra_tags="register")
            return redirect('/login_page#toregister')
        pw_hash = bcrypt.hashpw(
            request.POST["password"].encode(), bcrypt.gensalt())
        new_user = User.objects.create(
            first_name=first_name, last_name=last_name, username=username, email=email, password=pw_hash)
        request.session["new_user_id"] = new_user.id
        request.session["username"] = request.POST["username"]
    return redirect('/registration')


def registration(request):
    context = {
        "reg_user": User.objects.get(id=request.session["new_user_id"]),
    }
    return render(request, 'coaching_app/create_profile.html', context)


def login_process(request):
    matched_user = User.objects.filter(username=request.POST['username'])
    print(matched_user)
    if len(matched_user) < 1:
        messages.error(
            request, 'Email or password does not match', extra_tags="login")
        return redirect('/login_page')
    if bcrypt.checkpw(request.POST['password'].encode(), matched_user[0].password.encode()):
        request.session['username'] = request.POST['username']
        return redirect('/login')
    else:
        messages.error(request, 'Email or password do not match',
                       extra_tags="login")
        return redirect('/login_page')
    return redirect('/login_page')


def login(request):
    context = {
        "reg_user": User.objects.filter(username=request.session["username"])[0]
    }
    return render(request, 'coaching_app/everyone_account.html', context)


def logout(request):
    request.session.clear()
    return redirect('/login_page')


def survey(request):
    return render(request, "coaching_app/survey.html")


def survey_reply(request):
    return render(request, "coaching_app/congrats.html")


def my_account(request):
    context = {
        "reg_user": User.objects.filter(username=request.session["username"])[0],
        # "new_user": User.objects.get(id=userid)
    }
    return render(request, "coaching_app/my_account.html", context)


def user_account(request):
    return render(request, "coaching_app/user_account.html")


def no_survey_reply(request):
    return render(request, "coaching_app/no_survey_reply.html")

def update(request, userid):
    errors = User.objects.edit_validator(request.POST)
    user_id = userid
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/registration')
    matched_user = User.objects.filter(username=request.POST["username"])
    if len(matched_user) > 1:
        messages.error(request, 'Username unavailable')
        return redirect('/registration')
    else:
        updated_user = User.objects.get(id = userid)
        updated_user.first_name = request.POST['first_name']
        updated_user.last_name = request.POST['last_name']
        updated_user.bio = request.POST['bio']
        updated_user.email = request.POST['email']
        updated_user.username = request.POST['username']
        # updated_user.password = request.POST['password']
        updated_user.save()
    return redirect('/user/edit/'+ user_id)

def edit_account(request, userid):
    context = {
        "reg_user": User.objects.get(id=request.session["new_user_id"]),
        "new_user": User.objects.get(id=userid)
    }
    return render(request, "coaching_app/my_account.html", context)

