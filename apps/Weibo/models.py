from django.db import models


class WeiboArticle(models.Model):
    username = models.CharField(max_length=30, verbose_name='用户名')
    article = models.CharField(max_length=500, verbose_name='文章')
    # 点赞，评论，转发,帖子
    likes_num = models.IntegerField(verbose_name='点赞数')
    comment_num = models.IntegerField(verbose_name='评论数')
    transmit_num = models.IntegerField(verbose_name='转发数')
    c_time = models.CharField(max_length=50, verbose_name='最后回复时间')
    pic_links = models.CharField(max_length=500, verbose_name='图片链接', null=True, blank=True)
    art_links = models.CharField(max_length=200, verbose_name='文章链接', null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    modify_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    class Meta:
        verbose_name = '微博帖子'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{}".format(self.article)


class WeiboFirstComment(models.Model):
    username = models.CharField(max_length=30, verbose_name='用户名')
    context = models.CharField(max_length=500, verbose_name='评论内容')
    art = models.ForeignKey('WeiboArticle', on_delete=models.CASCADE, related_name='firstcomment', verbose_name="文章")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', null=True, blank=True)
    modify_time = models.DateTimeField(auto_now=True, verbose_name='修改时间', null=True, blank=True)

    class Meta:
        verbose_name = '微博一级评论'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{}：{}".format(self.username, self.context)


class WeiboSecondComment(models.Model):
    username = models.CharField(max_length=30, verbose_name='用户名')
    context = models.CharField(max_length=500, verbose_name='评论回复内容')
    com = models.ForeignKey('WeiboFirstComment', on_delete=models.CASCADE, related_name='secondcomment',
                            verbose_name="一级评论")
    art = models.ForeignKey('WeiboArticle', on_delete=models.CASCADE, related_name='secondcomment', verbose_name="文章")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', null=True, blank=True)
    modify_time = models.DateTimeField(auto_now=True, verbose_name='修改时间', null=True, blank=True)

    class Meta:
        verbose_name = '微博二级评论'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{}：{}".format(self.username, self.context)
