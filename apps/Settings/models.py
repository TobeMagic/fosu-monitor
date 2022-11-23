from django.db import models

# Create your models here.
from django.utils.html import format_html


class ClassType(models.Model):

    # 动态获取班级
    def __init__(self, *args, **kwargs):
        super(ClassType, self).__init__(*args, **kwargs)
        self._meta.get_field("class_teacher").choices = get_teacher_list()

    class_name = models.CharField(max_length=50, null=True, verbose_name='班级')
    class_teacher = models.CharField(choices=None, max_length=50, null=True, verbose_name='分管辅导员')

    class Meta:
        verbose_name = '班级'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.class_name


def get_class_type_list():
    return ClassType.objects.values_list('class_name', 'class_name')


class TeacherType(models.Model):
    teacher_name = models.CharField(max_length=50, null=True, verbose_name='姓名')
    teacher_server_chan_url = models.CharField(max_length=200, null=True, verbose_name='server chan URL')

    class Meta:
        verbose_name = '辅导员'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.teacher_name


def get_teacher_list():
    return TeacherType.objects.values_list('teacher_name', 'teacher_name')


