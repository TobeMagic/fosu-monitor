from django.contrib import admin
from .models import *
from django.utils.safestring import mark_safe


class WeiboFirstCommentInline(admin.StackedInline):
    model = WeiboFirstComment
    fields = ['art', ]
    readonly_fields = ['username']


class WeiboSecondCommentInline(admin.StackedInline):
    model = WeiboSecondComment
    fields = ('com',)
    readonly_fields = ['com']


@admin.register(WeiboArticle)
class WeiboArticleAdmin(admin.ModelAdmin):
    list_display = ['username', 'article', 'likes_num', 'comment_num', 'create_time', 'url_tag', 'img_tag']
    readonly_fields = ['username', 'article', 'likes_num', 'comment_num', 'create_time', 'url_tag', 'img_tag',
                       'transmit_num']
    exclude = ('pic_links', 'art_links')
    inlines = [WeiboFirstCommentInline, WeiboSecondCommentInline]
    date_hierarchy = 'create_time'  # 根据创建时间划分等级
    ordering = ['-create_time', ]  # 默认按照最新时间排序

    def url_tag(self, obj):
        if obj.art_links:
            return mark_safe(
                f'<a href="{obj.art_links}" target="_blank" >微博帖子地址</a>')
        return '-'

    url_tag.short_description = '微博帖子地址'

    def img_tag(self, obj):
        img_html = ''
        if obj.pic_links != '':
            img_list = obj.pic_links.split(';')
            img_list.remove(img_list[len(img_list) - 1])  # 删除最后一个空元素
            for img in img_list:
                img_html += f'<image src="{img}" style="width:160px; height:160px;" alt="图片" />'
            return mark_safe(img_html)
        return '-'

    img_tag.short_description = '微博帖子图片'


@admin.register(WeiboFirstComment)
class WeiboFirstCommentAdmin(admin.ModelAdmin):
    list_display = ['username', 'context', 'art']
    inlines = [WeiboSecondCommentInline]
    readonly_fields = ['username', 'context', 'art']
    list_display_links = ('username',)
    date_hierarchy = 'create_time'  # 根据创建时间划分等级
    ordering = ['-create_time', ]  # 默认按照最新时间排序
    search_fields = ('username', 'context')  # 设置搜索栏范围，如果有外键，要注明外键的哪个字段，双下划线


@admin.register(WeiboSecondComment)
class WeiboSecondCommentAdmin(admin.ModelAdmin):
    list_display = ['username', 'context', 'com']
    readonly_fields = ['username', 'context', 'com']
    date_hierarchy = 'create_time'  # 根据创建时间划分等级
    ordering = ['-create_time', ]  # 默认按照最新时间排序
    search_fields = ('username', 'context')  # 设置搜索栏范围，如果有外键，要注明外键的哪个字段，双下划线
    search_help_text = '搜索用户'  # 搜索提示文本， 默认为False
