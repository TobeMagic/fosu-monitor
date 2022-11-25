from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.contrib import messages

## user create
from myaccount.forms import ResetPasswordForm
from myaccount.models import UserProfile
from myaccount.forms import ProfileForm

### allauth
from allauth.utils import build_absolute_uri
from allauth.account.utils import user_pk_to_url_str
from allauth.account.forms import default_token_generator
from allauth.account.views import PasswordResetView



@login_required
def profile_update(request):
    """
    更新拓展用户的信息
    """
    user = request.user
    user_profile = get_object_or_404(UserProfile, user=user)

    if request.method == "POST":
        form = ProfileForm(request.POST)

        if form.is_valid():
            user.first_name = form.cleaned_data['name']
            user.save()
            user_profile.name = form.cleaned_data['name']
            # user_profile.identity_card = form.cleaned_data['identity_card']
            user_profile.telephone = form.cleaned_data['telephone']
            user_profile.classes = form.cleaned_data['classes']
            user_profile.gender = form.cleaned_data['gender']
            user_profile.save()
            messages.add_message(request, messages.SUCCESS, '个人信息更新成功！')
            return HttpResponseRedirect(reverse('myaccount:profile'))
    else:
        default_data = {
            'identity_card': user_profile.identity_card,
            'telephone': user_profile.telephone,
            'classes': user_profile.classes,
            'gender': user_profile.gender,
            'name':user_profile.name,
        }
        form = ProfileForm(default_data)

    return render(request, 'account/profile_update.html',
                  {'form': form, 'user': user})


class CustomPasswordResetView(PasswordResetView):

    def post(self, request, *args, **kwargs):
        reset_password_form = ResetPasswordForm(request.POST)
        if reset_password_form.is_valid():
            # 取到学号和身份证之后取到用户对象
            username = reset_password_form.cleaned_data['username']
            #identity_card = reset_password_form.cleaned_data['identity_card']
            user = User.objects.get(username=username)
            # 生成token
            token_generator = kwargs.get(
                "token_generator", default_token_generator)
            temp_key = token_generator.make_token(user)
            path = reverse(
                "account_reset_password_from_key",
                kwargs=dict(uidb36=user_pk_to_url_str(user), key=temp_key),
            )
            # url = build_absolute_uri(request, path)
            # print(url)
            # 重定向至修改密码链接
            return redirect(path)
        else:
            messages.add_message(request, messages.ERROR, '学号或身份证后八位填写错误！')
            # return render(request, 'identity_card_error.html')
            # return render(request,'account/password_reset.html', )
            return redirect('/accounts/password/reset/')