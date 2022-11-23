from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth.models import User
from django import forms
from myaccount.models import UserProfile

# from allauth.account.forms import ResetPasswordForm

from myaccount.models import GENDER_TYPES
from Settings.models import ClassType
from Settings.models import get_class_type_list


class ProfileForm(forms.Form):
    """
    用户可更新的信息
    """

    # 保证每次访问重新获取最新数据
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields["classes"].widget.choices = ClassType.objects.values_list('class_name', 'class_name')

    name = forms.CharField(label='姓名', max_length=50, required=True,
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    telephone = forms.CharField(label='手机号码', max_length=50, required=False,
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    # identity_card = forms.CharField(label='身份证号码', max_length=18,required=True)
    classes = forms.CharField(
        label='所在班级',
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    gender = forms.ChoiceField(
        label='性别',
        choices=GENDER_TYPES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )


class SignupForm(forms.Form):
    # 注册表单
    def signup(self, request, user):
        user_profile = UserProfile()
        user_profile.user = user
        user.save()
        user_profile.save()


class ResetPasswordForm(forms.Form):
    """
    重置密码表单,要求验证身份证
    """
    username = forms.CharField(
        label='学号',
        max_length=20,
        required=True
    )
    identity_card = forms.CharField(
        label='身份证号码后8位',
        max_length=8,
        required=True)

    def clean_identity_card(self):
        # 取到学号
        username = self.cleaned_data['username']
        # 取到身份证号码
        identity_card = self.cleaned_data["identity_card"]

        # 在django自带的User中取到用户，对其之后的进行操作
        try:
            self.users = User.objects.get(username=username)
        except:
            raise forms.ValidationError(
                _("学号填写错误")
            )

        # 验证身份证后8位与该学号的身份证是否匹配
        userProflie = UserProfile.objects.get(user=self.users)
        if userProflie.identity_card != identity_card:
            raise forms.ValidationError(
                _("身份证后八位填写错误")
            )
        return self.cleaned_data["identity_card"]

    def save(self, request, **kwargs):
        return self.cleaned_data['identity_card']
