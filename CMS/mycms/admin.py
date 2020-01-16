from django.contrib import admin
from mycms.models import *
# Register your models here.

class CMSAdmin(admin.ModelAdmin):
    # 如果想要显示其他表里面的字段 比如显CMS_user表里面的signature
    list_display = ('title','summary','content','author','show_signature','create_time','update_time')
    # 过滤 按照什么显示
    list_filter = ('create_time',)
    # 搜索 设置可以根据什么来搜索 这里如果连接了外键的要像这样显示代表了主表的字段user__username
    search_fields = ('title','author__user__username')
    # 通过这种方法来显示其他表的内容
    def show_signature(self,obj):
        return obj.author.signature
    # 这个是为这个函数的结果起名字，也就是起字段名
    show_signature.short_description = 'signature'
class ComentAdmin(admin.ModelAdmin):
    list_display = []

class UserAdmin(admin.ModelAdmin):
    list_display = ['user','signature']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
admin.site.register(CMS,CMSAdmin)
admin.site.register(Comment,ComentAdmin)
# admin.site.register(CMS_user,UserAdmin)
admin.site.register(CMS_user,UserAdmin)
admin.site.register(Category,CategoryAdmin)