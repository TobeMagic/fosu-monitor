from django.urls import re_path,path
from myaccount import views

app_name = "myaccount"
urlpatterns = [
    re_path(r'^profile/update/$', views.profile_update, name='profile_update'),
]