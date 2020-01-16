from django import forms
from DjangoUeditor.models import UEditorField


class MyUeditor(forms.Form):
    content = UEditorField('内容', width=600, height=400, toolbars='full', imagePath="images/", filePath="files",
                           upload_settings={"imageMaxSize": 1204000, }, settings={}, command=None, blank=True)


class UserForm(forms.Form):
    username = forms.CharField(
        label='用户名', max_length=10, min_length=4,
        error_messages={
            'require': '请输入用户名,至少四个字符，最多十个字符'
        },
        widget=forms.TextInput(attrs={'placeholder': '请输入用户名最少四位'})

    )
    password = forms.CharField(
        label='密 码', max_length=20, min_length=5,
        error_messages={
            'require': '请输入密码,长度在3到20字符之间',
        },
        required=True,
        widget=forms.TextInput(attrs={'placeholder': '请输入密码'})
    )
    # password_cf=forms.CharField(
    #     widget=forms.TextInput(attrs={'placeholder':'重复输入密码'})
    #
    # )
    # email = forms.EmailField(
    #     label='邮箱',
    #     max_length=50,
    #     widget=forms.EmailInput(attrs={'placeholder':'电子邮箱，用于找回密码'})
    # )


class change_password_form(forms.Form):
    password_old = forms.CharField(label='旧密码', max_length=10, min_length=3,
                                   error_messages={
                                       'require':'不能为空',
                                       'min_length':'大于3个字符',
                                       'max_length':'小于10个字符'

                                   },
                                   widget=forms.PasswordInput(attrs={'placeholder': '请输入旧密码'}))

    password_new = forms.CharField(label='新密码', max_length=10, min_length=3,
                                   error_messages={
                                       'require': '不能为空',
                                       'min_length': '大于3个字符',
                                       'max_length': '小于10个字符'

                                   },
                                   widget=forms.PasswordInput(attrs={'placeholder': '请输入新密码,最少3位数字或字母'
                                                                     }))
    password_new_yz = forms.CharField(label='确认新密码', max_length=10, min_length=3,
                                      error_messages={
                                          'require': '不能为空',
                                          'min_length': '大于3个字符',
                                          'max_length': '小于10个字符'

                                      },
                                      widget=forms.PasswordInput(attrs={'placeholder': '请重复新密码'
                                                                        }))
