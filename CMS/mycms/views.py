from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from mycms.models import *
# Create your views here.
from django.contrib import auth
from django.contrib.auth import authenticate
from django_comments.models import Comment
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password


@login_required()  # 调用的是accounts_login接口，需要设置accounts/login路由
def index(request):
    # print(request.user)
    # print(request.user.username)
    # 按照时间倒排
    user = request.user
    userinfo = CMS_user.objects.all()
    infos = CMS.objects.all().order_by('-create_time')
    categories = Category.objects.all()
    status = 'active'

    # print(infos)
    # print(categories)
    return render(request, 'index.html', {'infos': infos,
                                          'userinfo': userinfo,
                                          'user': request.user,
                                          'categories': categories,
                                          'status': status
                                          })


def search_q(request):

    keyword = request.GET.get('q')
    cms = CMS.objects.filter(title__contains=keyword)
    categories = Category.objects.all()
    status = 'active'
    return render(request, 'index.html', {'infos': cms,
                                          'user': request.user,
                                          'categories': categories,
                                          'status': status
                                          })
def search(request):
    return render(request,'search.html')
    # cms = CMS.objects.filter(title__contains=keyword)
    # categories = Category.objects.all()
    # status = 'active'
    # return render(request, 'index.html', {'infos': cms,
    #                                       'user': request.user,
    #                                       'categories': categories,
    #                                       'status': status
    #                                       })


def detail(request, id):
    detail = CMS.objects.get(id=id)
    # print(detail)
    veiw_count = CMS.objects.get(id=id)
    veiw_count.view_count = veiw_count.view_count + 1
    print(veiw_count.view_count)
    veiw_count.save()
    return render(request, 'detail.html', {'detail': detail, 'user': request.user})


def login(request):
    return render(request, 'login.html')


def acc_login(request):
    username = request.POST.get('user')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)  # 判断登录的人是否认证 在user表里面
    print(user)
    if user is not None:
        auth.login(request, user)  # 这个作为用户的session保存和django自带的用户登录
        return redirect('/cms/index/')
    else:
        return render(request, 'login.html', {'error': '用户名或者密码错误'})


def logout(request):
    user = request.user

    auth.logout(request)
    return redirect('/login/')


def pub_comment(request):
    # print(request.POST)
    comment = request.POST.get('comments')
    cms_id = request.POST.get('cms_id')
    # print(cms_id)
    user_id = CMS_user.objects.filter(user__username=request.user)  # 这个是前端传回来的user，也就是现在登录的人，只有登录才可以发表评论
    content_type_id = '11'  # 这个是每个表的id，这个id数据cms表的id
    object_pk = cms_id  # 前端传回发表的帖子的id
    Comment.objects.create(
        object_pk=object_pk,
        site_id=1,
        content_type_id=11,
        user=request.user,
        comment=comment,
    )
    return redirect('/cms/detail/%s' % cms_id)


# 通过类别显示
def show_category(request, id):
    infos = CMS.objects.filter(category=id)
    categories = Category.objects.all()
    # print(infos)
    # print(type(id))
    return render(request, 'index.html', {'infos': infos,
                                          'user': request.user,
                                          'categories': categories,
                                          'category_id': int(id)
                                          })


# from mycms.forms import MyUeditor
def pub_content(request):
    categories = Category.objects.all()
    return render(request, 'pub_content.html', locals())


def pub_success(request):
    user = request.user
    print(user)
    title = request.POST.get('title')
    print(title)
    summary = request.POST.get('summary')
    print(summary)
    content = request.POST.get('editorValue')
    print(content)
    author = request.POST.get('author')
    '''
    如果是get里面是user=author就会报错，
    查询查询的是外键最终的表的字段，每个表里面用__隔开,
    外键，要传进去实例,查找和修改和增加都是在子表里面插入实例。
    '''
    author = CMS_user.objects.get(user__username=author)  # 如果是get里面是user=author就会报错，
    # 查询查询的是外键最终的表的字段，每个表里面用__隔开
    category = request.POST.get('category')
    print(category)
    category = Category.objects.get(name=category)  # 这是一个实例
    if title:
        # 如果是外键，要传进去实例

        CMS.objects.create(title=title,
                           summary=summary,
                           content=content,
                           author=author,
                           category=category,
                           )
        return redirect('/cms/index/')


def register(request):
    return render(request, 'register.html')


def register_check(request):
    # print(request.POST)
    user = request.POST.get('user')
    password = request.POST.get('password')
    username = User.objects.filter(username=user)
    if username:
        info = '抱歉，您这个用户已经存在了'
        return render(request, 'register.html', {'error': info})
    else:
        # create创建的是明文密码 create_user创建的加密的
        new_user = User.objects.create_user(username=user,
                                            password=password,
                                            )
        user = User.objects.get(username=user)
        CMS_user.objects.create(user=user)
        new_user.save()
        # 自动给你的user表自动校验
        # user = authenticate(username=user,
        #                          password=password, )
        # print('login',user)
        # 添加sessions
        # auth.login(request, user)
        return redirect('/login/')


from mycms.forms import UserForm, change_password_form
from django.contrib.auth.hashers import check_password


# django自带form表单验证 学习使用
def verrify(username, password):
    error = {}
    if len(username) <= 0:
        error['username'] = '用户名不能为空'
    if len(username) > 8:
        error['username'] = '字符不能超过六个'
    if len(password) < 3:
        error['password'] = '长度不能小于3'
    if len(password) > 10:
        error['password'] = '长度不能超过10'
    return error


def login_in(request):
    if request.method == 'POST':
        print(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        a = verrify(username, password)
        print(a)
        if verrify(username, password) != {}:
            error = verrify(username, password)
            uf = UserForm(request.POST)
            return render(request, 'mycms/login_in.html', locals())
        uf = UserForm(request.POST)
        print(uf.is_valid())
        if uf.is_valid():  # 这一步是检验form表单里面有没有内容，有则为true。
            a = uf.is_valid()  # false。不用 is_valid()，是因为form里有4个字段，而这里只用2个，false。
            username = uf.cleaned_data['username']  # 只有验证后，才能使用cleaned_data方法，即使是验证 false。
            print(username)
            password = uf.cleaned_data['password']
            print(password)
            print(uf.cleaned_data)
            has_username = User.objects.filter(username=username)
            if has_username:
                get_password = has_username[0].password
                print(get_password)
                check_pd = check_password(password, get_password)
                if check_pd:
                    return redirect('/cms/index/')
                else:
                    error = True
                    return render(request, 'mycms/login_in.html', locals())
            else:
                error = True
                return render(request, 'mycms/login_in.html', locals())
        else:
            error = True
            return render(request, 'mycms/login_in.html', locals())
    else:
        uf = UserForm()
        print(uf)
        return render(request, 'mycms/login_in.html', locals())


def Person_info(request):
    user = request.user
    userinfo = CMS_user.objects.get(user=user)
    print(userinfo.photo)
    return render(request, 'person_info.html', locals())


def changepassword(request):
    if request.method == 'POST':
        form = change_password_form(request.POST)

        if form.is_valid():
            user = request.user
            password_old = form.cleaned_data['password_old']
            password_bt = form.cleaned_data['password_new_yz']
            password = form.cleaned_data['password_new']
            obj = User.objects.filter(username=user)
            if obj:
                print(obj[0].password)
                sure_password = check_password(password_old, obj[0].password)
                print(sure_password)
                if sure_password:
                    if password_old == password:
                        error = '您修改前后的密码一致，请重新输入新的密码'
                        password_old = form.cleaned_data['password_old']
                        password_bt = form.cleaned_data['password_new_yz']
                        password = form.cleaned_data['password_new']
                        userinfo = CMS_user.objects.get(user=user)
                        if password != password_bt:
                            errors = '您新密码两次输入的密码不一致'
                            password_old = form.cleaned_data['password_old']
                            password_bt = form.cleaned_data['password_new_yz']
                            password = form.cleaned_data['password_new']
                            userinfo = CMS_user.objects.get(user=user)
                            return render(request, 'mycms/change_password.html', locals())
                        return render(request, 'mycms/change_password.html', locals())
                    else:
                        if password != password_bt:
                            error = '您新密码两次输入的密码不一致'
                            form = change_password_form(request.POST)
                            return render(request, 'mycms/change_password.html', locals())
                        obj[0].set_password(password)
                        obj[0].save()
                        userinfo = CMS_user.objects.get(user=user)
                        return render(request, 'mycms/change_success.html', locals())
                else:
                    error = '您输入的旧密码错误，请重新输入'
                    password_old = form.cleaned_data['password_old']
                    password_bt = form.cleaned_data['password_new_yz']
                    password = form.cleaned_data['password_new']
                    return render(request, 'mycms/change_password.html', locals())

            else:
                pass
        else:
            errors = form.errors
            return render(request, 'mycms/change_password.html', {'errors': errors, 'form': form})
    else:
        form = change_password_form()
        errors = form.errors
        user = request.user
        userinfo = CMS_user.objects.get(user=user)
        return render(request, 'mycms/change_password.html', locals())


def change_success(request):
    return render(request, 'mycms/change_success.html')


def manage(request):
    user = request.user
    status = 'active'
    # 在新增的时候要添加实例，查找的时候只需要找外键所对应表的字段。
    infos = CMS.objects.filter(author__user__username=user).order_by('-create_time')
    categories = Category.objects.filter(administrator__user__username=user)
    return render(request, 'mycms/display_cms.html', locals())


# def person_cms(request):
#     user = request.user
#     status = 'active'
#     # 在新增的时候要添加实例，查找的时候只需要找外键所对应表的字段。
#     infos = CMS.objects.filter(author__user__username=user).order_by('-create_time')
#     categories = Category.objects.filter(administrator__user__username=user)
#     return render(request, 'mycms/display_cms.html', {'infos': infos,
#                                           'user': request.user,
#                                           'categories': categories,
#                                           'status': status
#                                           })

def person_category(request, id):
    user = request.user
    infos = CMS.objects.filter(category=id)
    categories = Category.objects.filter(administrator__user__username=user)
    # print(infos)
    # print(type(id))
    return render(request, 'mycms/display_cms.html', {'infos': infos,
                                                      'user': request.user,
                                                      'categories': categories,
                                                      'category_id': int(id)
                                                      })


@login_required()
def delete_cms(requset, id):
    user = requset.user
    cms = CMS.objects.get(id=id)
    if user.username == cms.author.user.username:
        cms.delete()
        return redirect('/cms/manage')
        # return JsonResponse({'code':6666,'status':'success'})
    else:
        return JsonResponse({'code': 7777, 'status': 'delete failure'})


def change_info(request):
    pass
