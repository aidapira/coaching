from django.conf.urls import url
from . import views
                    
urlpatterns = [
    url(r'^login_page$', views.login_page),
    url(r'^regprocess$', views.user_process),
    url(r'^registration$', views.registration),
    url(r'^loginprocess$', views.login_process),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^$', views.home_page),
    url(r'^survey$', views.survey),
    url(r'^survey_reply$', views.survey_reply),
    url(r'^my_account$', views.my_account),
    url(r'^user_account$', views.user_account),
    url(r'^no$', views.no_survey_reply),
    url(r'^user/update/(?P<userid>\w+)$', views.update),
    url(r'^user/edit/(?P<userid>\w+)$', views.edit_account),
    # url(r'^createpost$', views.createpost),
    url(r'^sampleworkout$', views.sampleworkout),
    url(r'^search', views.search),
    # url(r'^createpost$', views.createpost)
    url(r'^search', views.search),
    url(r'^createpost$', views.create_post)
]

