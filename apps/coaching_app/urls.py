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
    url(r'^survey_reply$', views.survey_reply)
]