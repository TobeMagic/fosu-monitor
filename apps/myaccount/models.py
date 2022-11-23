from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from allauth.account.models import EmailAddress
from Settings.models import get_class_type_list

GENDER_TYPES = (
    ('男', '男'),
    ('女', '女')
)


class UserProfile(models.Model):
    """
    a.姓名
    b.学号
    c.班级
    d.性别
    e.身份证
    """
    def __init__(self, *args, **kwargs):
        super(UserProfile, self).__init__(*args, **kwargs)
        self._meta.get_field("classes").choices = get_class_type_list() # 动态链接Setting中所存在的班级

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='用户')
    name = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name='姓名')
    identity_card = models.CharField(
        max_length=18, blank=True, null=True, verbose_name='身份证后八位')
    telephone = models.CharField(max_length=50, blank=True, null=True, verbose_name='手机')
    classes = models.CharField(
        choices=None,
        max_length=50,
        blank=True,
        verbose_name='所在班级')
    gender = models.CharField(
        choices=GENDER_TYPES,
        max_length=50,
        null=True,
        blank=True,
        verbose_name='性别')

    mod_date = models.DateTimeField(auto_now=True, verbose_name='最后修改时间')

    class Meta:
        verbose_name = '个人信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{}".format(self.user.__str__())


class ImportUser(models.Model):
    import_file = models.FileField(verbose_name='上传文件', upload_to='upload/')
    handle_text = models.TextField(verbose_name='处理信息', null=True, blank=True)

    class Meta:
        verbose_name = '批量导入用户信息'
        verbose_name_plural = verbose_name
