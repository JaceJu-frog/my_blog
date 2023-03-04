# 引入表单类
from django import forms
# 引入User模型
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Profile
from django.contrib.auth.forms import UserCreationForm


# 登录表单，继承了forms.Form类，不与数据库直接接触。
class UserLoginForm(forms.Form):

    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)



class UserRegisterForm(UserCreationForm):

    email = forms.EmailField(label="Email")

    class Meta:
        # 表示模型来自django自带的User
        model = User
        #展示的字段
        fields = ['id','username', 'email']

# 新建一个表单以编辑用户信息
class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('phone', 'avatar', 'bio')


