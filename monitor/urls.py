"""monitor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from myaccount.views import CustomPasswordResetView
from Tieba import views
from Weibo import views

urlpatterns = [
    path('', admin.site.urls),
    path('accounts/password/reset/', CustomPasswordResetView.as_view()),
    # path('accounts/', include('allauth.urls')),
    path('accounts/', include('myaccount.urls')),
]

admin.site.site_header = "佛山科学技术学院舆情监测平台"
admin.site.site_title = "佛山科学技术学院舆情监测平台"
admin.site.index_title = "欢迎进入佛山科学技术学院舆情监测平台"
