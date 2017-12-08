from django.contrib import admin
from .models import Category,Tag,Post
from comments.models import Comment
from django.contrib.flatpages.admin import FlatPageAdmin , FlatpageForm
from django.contrib.flatpages.models import FlatPage
from django.db import models
from django.db.models import Count

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

	list_display=['title','created_time','author','category','comment_count']
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
	
	def get_queryset(self,request):
		qs = super(Postadmin,self).get_queryset(request)
		return qs.annotate(comment_count=Count('comment'))

	def comment_count(self,inst):
		return inst.comment_count
	comment_count.admin_order_field = 'comment_count'
'''
通过在admin中调用get_queryset方法并配合admin_order_field来实现comment_count的显示
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
