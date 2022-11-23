# coding:utf8
from django.contrib import admin

# Register your models here.
from Settings.models import ClassType, TeacherType

# 将应用注册到admin,使得admin能对其进行管理
admin.site.register(ClassType)
admin.site.register(TeacherType)
