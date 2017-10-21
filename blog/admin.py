from django.contrib import admin
from .models import Category,Tag,Post

class Postadmin(admin.ModelAdmin):
	list_display=['title','created_time','modified_time','author','category']

admin.site.register(Post,Postadmin)
admin.site.register(Category)
admin.site.register(Tag)
