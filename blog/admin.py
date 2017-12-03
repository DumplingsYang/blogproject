from django.contrib import admin
from .models import Category,Tag,Post 
from comments.models import Comment
from django.contrib.flatpages.admin import FlatPageAdmin , FlatpageForm
from django.contrib.flatpages.models import FlatPage
from django.db import models

class CommentInline(admin.TabularInline):
	model = Comment
	extra = 0
	readonly_fields = ('created_time','name','email','text')
	exclude = ('url',)
	verbose_name = 'comments list'
	verbose_name_plural = 'comments list'
'''
在posts inline 中 显示只读created_time
'''
class Postadmin(admin.ModelAdmin):
	list_display=['title','created_time','author','category']
	fieldsets=[
			('Posts',{'fields':['title','body','author']}),
			('Time',{'fields':['created_time','modified_time']}),
			('Others',{'fields':['excerpt','category','post_slug']})
	]
	inlines = [CommentInline]
	list_filter = (
        ('author', admin.RelatedOnlyFieldListFilter),
        ('created_time')
    )
	search_fields = ['title','body']
	save_as = True

'''class CustomFlatpage(FlatPage):
	class Meta:
		verbose_name_plural = ('About page')
尝试修改flatpage在admin上的名字，但更改之后它好像会在数据库重新创建一个表单，
目前无法解决这个问题，同样尝试修改默认field，也没有 2017.11.26
'''
class CustomFlatPageAdmin(FlatPageAdmin):
    fieldsets = (
        (None, {'fields': ('url', 'title', 'content',)}),
        (('Advanced options'), {
            'classes': ('collapse',),
            'fields': ('registration_required', 'template_name'),
        }),
)
admin.site.register(Post,Postadmin)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.unregister(FlatPage)
admin.site.register(FlatPage,CustomFlatPageAdmin)	
