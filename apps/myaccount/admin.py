import re
from django.contrib.auth.models import User
from django.contrib import admin, messages
import pandas as pd
from myaccount.models import UserProfile, ImportUser


class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'name',
        'gender',
        'classes',
        'telephone',
        'mod_date')
    search_fields = (
        'name',
    )
    list_filter = [
        'classes'
    ]


# # 定义一个行内 admin
# class ProfileInline(admin.StackedInline):
#     model = UserProfile
#     can_delete = False
#     verbose_name_plural = 'UserProfile'
#
# # 将 Profile 关联到 User 中
# class UserAdmin(BaseUserAdmin):
#     inlines = (ProfileInline,)


class ImportUserAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        # 先保存，再进入后续操作
        obj.save()
        # 读取导入的文件
        file_path = 'appendix/{}'.format(obj.import_file)
        df = pd.read_excel(file_path)
        # 检查学号是否已经注册过
        existed_people = []
        df['证件号码'] = df['证件号码'].astype(str)
        for i in range(len(df['学号'])):
            stu_id = df['学号'][i]
            try:
                User.objects.get(username=stu_id)
                existed_people.append(df['姓名'][i])
            except:
                pass

        if existed_people:
            # 得到未提交列表
            error_type = '用户信息已存在'
            for people in existed_people:
                error_message = '导入失败，{}已注册过账号，请检查后重新上传'.format(people)
                messages.error(request, error_message)
            return False

        # 检查是否有空值，
        check_list = df.isnull().any().tolist()
        if True in check_list:
            error_message = '数据中存在空值，请仔细检查后导入'
            messages.error(request, error_message)
            return False
        # 检查身份证号是否正确
        for i in range(len(df['证件号码'])):
            identity_card_check = re.sub("[^A-Za-z0-9]+", '', df['证件号码'][i])
            if len(identity_card_check) != 18:
                error_message = '导入失败:身份证号长度有误，请确认！'
                messages.error(request, error_message)
                return False

        # 检查完毕，开始导入
        for i in range(len(df)):
            username = int(df['学号'][i])
            name = str(df['姓名'][i].strip())
            classes = df["班别"][i]
            identity_card = re.sub("[^A-Za-z0-9]+", '', df['证件号码'][i])[10:]
            password = identity_card
            if int(df['证件号码'][i][16]) % 2 == 0:
                gender = '女'
            else:
                gender = '男'

            User.objects.create_user(
                username=username,
                password=password,
                first_name=name,
            )
            # 获取创建的用户在django自带用户系统中的id，后续外键绑定需要用到
            pk = User.objects.get(username=username)

            UserProfile.objects.create(
                user=pk,
                name=name,
                classes=classes,
                identity_card=identity_card,
                gender=gender
            )

            text = '{}({})成功导入({}/{})'.format(name, df['学号'][i], i + 1, len(df))
            messages.success(request, text)


# 重新注册 User
admin.site.register(ImportUser, ImportUserAdmin)
# admin.site.unregister(User)
# admin.site.register(User, UserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
