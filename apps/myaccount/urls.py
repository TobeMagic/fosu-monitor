from django.urls import re_path,path
from myaccount import views
from allauth.account.urls import views as allauth_views
app_name = "myaccount"
urlpatterns = [
    re_path(r'^profile/$', views.profile_update, name='profile_update'),

    # 以下url源自allauth.account.urls
    path("logout/", allauth_views.logout, name="account_logout"),
    path(
        "password/change/",
        allauth_views.password_change,
        name="account_change_password",
    ),
    path("password/set/", allauth_views.password_set, name="account_set_password"),
    path("inactive/", allauth_views.account_inactive, name="account_inactive"),
    path(
        "password/reset/done/",
        allauth_views.password_reset_done,
        name="account_reset_password_done",
    ),
    re_path(
        r"^password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$",
        allauth_views.password_reset_from_key,
        name="account_reset_password_from_key",
    ),
    path(
        "password/reset/key/done/",
        allauth_views.password_reset_from_key_done,
        name="account_reset_password_from_key_done",
    )
]