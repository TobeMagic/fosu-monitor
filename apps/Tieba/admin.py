from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import *
import re


#
# # 嵌入外键
class TiebaCommentInline(admin.StackedInline):
    model = BaiduComment
    readonly_fields = ['BaiduUser', 'BaiduPost', ]
    fields = ['BaiduPost', 'BaiduUser']


class TiebaPostInline(admin.StackedInline):
    model = BaiduPost
    readonly_fields = ['post_id', 'title', 'url', ]


class TiebaUserInline(admin.StackedInline):
    model = BaiduUser
    readonly_fields = ['username', 'url', ]


@admin.register(BaiduUser)
class BaiduUserAdmin(admin.ModelAdmin):
    # 展示列表
    list_display = ('username', 'url_tag', 'create_time')
    list_display_links = ('username',)
    readonly_fields = ['username', 'url', ]
    date_hierarchy = 'create_time'  # 根据创建时间划分等级
    ordering = ['-create_time', ]  # 默认按照最新时间排序
    search_fields = ('username',)  # 设置搜索栏范围，如果有外键，要注明外键的哪个字段，双下划线
    search_help_text = '搜索用户'  # 搜索提示文本， 默认为False
    list_filter = ['create_time', ]
    inlines = [TiebaCommentInline, ]

    def url_tag(self, obj):
        if obj.url:
            return mark_safe(  # obj.picture 是相对路径, obj.picture.url是完整路径
                f'<a href="{obj.url}" target="_blank" >用户贴吧地址</a>')
        return '-'

    url_tag.short_description = '贴吧用户地址'


@admin.register(BaiduPost)
class BaiduPostAdmin(admin.ModelAdmin):
    # 展示列表
    list_display = ('title', 'img_tag', 'url_tag', 'create_time')
    # list_display_links = ('title',)
    exclude = ('img_url',)
    search_fields = ('title',)  # 设置可搜索内容
    search_help_text = '搜索帖子'  # 搜索提示文本， 默认为False
    readonly_fields = ['post_id', 'title', 'url', ]
    date_hierarchy = 'create_time'  # 根据创建时间划分等级
    ordering = ['-create_time', ]  # 默认按照最新时间排序
    inlines = [TiebaCommentInline, ]

    list_filter = ['create_time', ]

    def img_tag(self, obj):
        img_html = ''
        if obj.img_url != '[]':
            temp = re.sub("'", '520', obj.img_url)
            img_list = re.findall('520(.*?)520', temp)  # 在字符串提取内容
            for img in img_list:
                img_html += f'<image src="{img}" style="width:80px; height:80px;" alt="图片" />'
            return mark_safe(img_html)
        return '-'

    img_tag.short_description = '帖子图片'

    def url_tag(self, obj):
        if obj.url:
            return mark_safe(f"<a href='{obj.url}' target='_blank'>{obj.url}</a>")
        return '-'

    url_tag.short_description = "帖子地址"


@admin.register(BaiduComment)
class BaiduCommentAdmin(admin.ModelAdmin):
    # 展示列表
    list_display = ('comment', 'BaiduPost', 'BaiduUser', 'create_time')
    # list_display_links = ('comment',)
    search_fields = ('comment', 'BaiduUser__username', 'BaiduPost__title')  # 设置搜索栏范围，如果有外键，要注明外键的哪个字段，双下划线
    search_help_text = '搜索帖子评论或者用户评论记录'  # 搜索提示文本， 默认为False
    readonly_fields = ['BaiduUser', 'comment', 'BaiduPost', ]
    date_hierarchy = 'create_time'  # 根据创建时间划分等级
    ordering = ['-create_time', ]  # 默认按照最新时间排序
    list_filter = ['create_time', ]
