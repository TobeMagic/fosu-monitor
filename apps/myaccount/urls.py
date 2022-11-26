from django.urls import re_path, path
from myaccount import views
from allauth.account.urls import views as allauth_views

app_name = "myaccount"
urlpatterns = [
    re_path(r'^profile/$', views.profile_update, name='profile_update'),

    # 以下url源自allauth.account.urls

]
