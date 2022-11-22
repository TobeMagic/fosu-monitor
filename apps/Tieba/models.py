from django.db import models
from django.utils.html import format_html


class BaiduUser(models.Model):
    """
    a. 用户名
    b. 贴吧用户`url`
    """
    username = models.CharField(max_length=128, verbose_name='贴吧用户名', blank=True, null=True)
    url = models.CharField(max_length=200, verbose_name='用户地址', blank=True, null=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', null=True, blank=True)
    modify_time = models.DateTimeField(auto_now=True, verbose_name='修改时间', null=True, blank=True)

    def __str__(self):
        return self.username

    class Meta:
        db_table = "baidu_user"
        verbose_name = '贴吧用户'
        verbose_name_plural = verbose_name  # 复数形式


class BaiduPost(models.Model):
    """
    a. 帖子唯一`id`
    b. 帖子标题
    c. 帖子照片路由
    d. 帖子路由`url`
    e. 一对多外键 → 评论
    """
    post_id = models.CharField(max_length=128, verbose_name='帖子ID', blank=True)
    title = models.CharField(max_length=1024, verbose_name='标题', blank=True)
    img_url = models.CharField(max_length=2048, verbose_name='图片', blank=True)
    url = models.CharField(max_length=200, verbose_name='帖子地址', blank=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    modify_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    def __str__(self):
        return self.title

    class Meta:
        db_table = "baidu_post"
        verbose_name = '贴吧贴子'
        verbose_name_plural = verbose_name  # 复数形式


class BaiduComment(models.Model):
    """
    a. 一对一外键 → 贴吧用户
    b. 内容
    c. 多对一外键 → 帖子
    """
    BaiduUser = models.OneToOneField(BaiduUser, on_delete=models.CASCADE, related_name="comment", verbose_name='百度用户')
    comment = models.CharField(max_length=2048, verbose_name='评论', blank=True)
    BaiduPost = models.ForeignKey(BaiduPost, on_delete=models.CASCADE, related_name="comment", verbose_name='对应帖子')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    modify_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    def __str__(self):
        return self.comment

    class Meta:
        db_table = "baidu_comment"
        verbose_name = '贴吧一级评论'
        verbose_name_plural = verbose_name  # 复数形式
