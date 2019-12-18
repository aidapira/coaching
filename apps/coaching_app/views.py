from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
from .models import *

import argparse

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# print(build)

developer_key = 'AIzaSyCVuN7GOKmyHIT0xtpd2WTM4n9pEI-zwXQ'
youtube_api_service_name = 'youtube'
youtube_api_version = 'v3'


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
        updated_user = User.objects.get(id=userid)
        updated_user.first_name = request.POST['first_name']
        updated_user.last_name = request.POST['last_name']
        updated_user.bio = request.POST['bio']
        updated_user.email = request.POST['email']
        updated_user.username = request.POST['username']
        # updated_user.password = request.POST['password']
        updated_user.save()
    return redirect('/user/edit/' + user_id)


def edit_account(request, userid):
    context = {
        "reg_user": User.objects.get(id=request.session["new_user_id"]),
        "new_user": User.objects.get(id=userid)
    }
    return render(request, "coaching_app/my_account.html", context)


def sampleworkout(request):
    return render(request, "coaching_app/sample_workout.html")


# def item(request):
    # print('*'*30)
    # print(request.POST["search"])

    # print('*'*30)

    # print(request.POST.results)

    # title = request.POST["title"]
    # print(title)
    # context = {
    #     "title": request.POST["title"],
    #     "videoid": request.POST["videoid"]
    # }
    # return render(request, "coaching_app/item.html", context)

def search(request):
    print('SEARCH ITEM', request.POST['search']),
    search = request.POST['search'],
    return redirect('/item')

# def item(request, options):
#     youtube = build(youtube_api_service_name, youtube_api_version,
#                     developerKey=developer_key)

#     search_response = youtube.search().list(
#         q=options,
#         part='id,snippet',
#         maxResults=1
#     ).execute()


#     videos = []
#     channels = []
#     playlists = []

#     for search_result in search_response.get('items', []):
#         if search_result['id']['kind'] == 'youtube#video':
#             videos.append('%s (%s)' % (search_result['snippet']['title'],
#                                         search_result['id']['videoId']))
#         elif search_result['id']['kind'] == 'youtube#channel':
#             channels.append('%s (%s)' % (search_result['snippet']['title'],
#                                         search_result['id']['channelId']))
#         elif search_result['id']['kind'] == 'youtube#playlist':
#             playlists.append('%s (%s)' % (search_result['snippet']['title'],
#                                             search_result['id']['playlistId']))

# #   print 'Videos:\n', '\n'.join(videos), '\n'
# #   print 'Channels:\n', '\n'.join(channels), '\n'
# #   print 'Playlists:\n', '\n'.join(playlists), '\n'


#     if __name__ == '__main__':
#         parser = argparse.ArgumentParser()
#         parser.add_argument('--q', help='Search term', default='Google')
#         parser.add_argument('--max-results', help='Max results', default=25)
#         args = parser.parse_args()

# #   try:
# #     youtube_search(args)
# #   except HttpError, e:
# #     print 'An HTTP error %d occurred:\n%s' % (e.resp.status, e.content)

# # def item(request):
#     # context = {
#     #     "title": request.POST['title'],
#     #     "videoid": request.POST['videoid']
#     # }
#     return render(request, "coaching_app/item.html")
