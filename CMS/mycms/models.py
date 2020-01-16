from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
# Create your models here.
from DjangoUeditor.models import UEditorField


# 内容
class CMS(models.Model):
    title = models.CharField(max_length=64)
    # blank = True 意思是填写表单的时候可以为空
    summary = models.CharField(max_length=256, blank=True, null=True)
    # 图片上传到collect_media里面，imagePath的配置，调节参数默认会带时间戳,文件上传的位置filePath
    # 详情https://github.com/twz915/DjangoUeditor3
    # 针对后台设置这个上传边框大小，如果是在setting里面设置了static_root，/
    # 则会从收集静态文件的文件夹（collect_static)找这个文件，如果没有设置，则从根目录的static文件夹下面找。
    content = UEditorField('内容', width=600, height=400, toolbars='full', imagePath="images/", filePath="files",
                           upload_settings={"imageMaxSize": 1204000001,},settings={},command=None, blank=True)
    # 如果所引用的外键在这个函数下面，则需要将外键名字用引号括起来就不会报错了
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    author = models.ForeignKey('CMS_user', on_delete=models.CASCADE)
    view_count = models.IntegerField(default=0)  # 观看次数
    ranking = models.IntegerField(default=0)  # 排名
    create_time = models.DateTimeField(auto_now_add=now)  # 这个时间不允许后面修改，在调用save的时候不会变。只有对这个字段进行update
    update_time = models.DateTimeField(auto_now=now)  # 这个时间，比如更改了任意一个时间，保存了就会发生变化。

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '发表内容'
        verbose_name_plural = verbose_name


# 评论
class Comment(models.Model):
    pass


# 板块
class Category(models.Model):
    # 唯一
    name = models.CharField(max_length=32, unique=True)
    administrator = models.ForeignKey('CMS_user', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '板块'
        verbose_name_plural = verbose_name


# 用户
class CMS_user(models.Model):
    # 一对一
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    signature = models.CharField(max_length=128, default='This guy is too lazy to leave anything here.')
    # upload_to意思是上传后将自动保存到 os.path.join(MEDIA_ROOT, upload_to)。这个文件是可变的，只要上传就会有
    photo = models.ImageField(upload_to='upload_imgs/', default="/img/1.jpg")

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name
