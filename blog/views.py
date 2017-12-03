#blog/views.py
from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404
from .models import Post,Tag,Category
from comments.forms import CommentForm
from django.views.generic import ListView,DetailView
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
from django.db.models import Q
import markdown

class IndexView(ListView):
	model=Post
	template_name='blog/index.html'
	queryset=Post.objects.order_by('-created_time')
	context_object_name='post_list'
	paginate_by=8

	def get_context_data(self,**kwargs):
		context=super().get_context_data(**kwargs)
		paginator=context.get('paginator')
		page=context.get('page_obj')
		is_paginated=context.get('is_paginated')
		pagination_data=self.pagination_data(paginator,page,is_paginated)
		context.update(pagination_data)
		return context
	def pagination_data(self,paginator,page,is_paginated):
		if not is_paginated:
			return {}
		left=[]
		right=[]
		left_has_more=False
		right_has_more=False
		first=False
		last=False
		page_number=page.number
		total_pages=paginator.num_pages
		page_range=paginator.page_range
		if page_number==1:
			right=page_range[page_number:page_number+2]
			if right[-1]<total_pages-1:
				right_has_more=True
			if right[-1]<total_pages:
				last=True
		elif page_number==total_pages:
			left=page_range[(page_number-3) if (page_number-3)>0 else 0:page_number-1]
			if left[0]>2:
				left_has_more=True
				if left[0]>1:
					first=True
		else:
			left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
			right=page_range[page_number:page_number+2]
			if right[-1]<total_pages-1:
				right_has_more=True
			if right[-1]<total_pages:
				last=True
			if left[0]>2:
				left_has_more=True
			if left[0]>1:
				first=True
		data={
			'left':left,
			'right':right,
			'left_has_more':left_has_more,
			'right_has_more':right_has_more,
			'first':first,
			'last':last,
		}
		return data
class CategoryViews(IndexView):
	def get_queryset(self):
		cate=get_object_or_404(Category,pk=self.kwargs.get('pk'))
		return super(CategoryViews,self).get_queryset().filter(category=cate)
class ArchivesViews(IndexView):
	def get_queryset(self):
		year=self.kwargs.get('year')
		month=self.kwargs.get('month')
		return super(ArchivesViews,self).get_queryset().filter(created_time__year=year,created_time__month=month)
class TagView(IndexView):
	'''model=Post
	template_name='blog/index.html'
	context_object_name='post_list'
	'''
	def get_queryset(self):
		tag=get_object_or_404(Tag,pk=self.kwargs.get('pk'))
		return super(TagView,self).get_queryset().filter(tags=tag)
'''class PostDetailView(DetailView):
	model=Post
	template_name='blog/detail.html'
	context_object_name='post'
	def get(self,request,*args,**kwargs):
		response=super(PostDetailView,self).get(request,*args,**kwargs)
		self.object.increase_views()
		return response
	def get_object(self,queryset=None):
		post=super(PostDetailView,self).get_object(queryset=None)
		md=markdown.Markdown(extensions=[
				'markdown.extensions.extra',
				'markdown.extensions.codehilite',
				TocExtension(slugify=slugify),

			])
		post.body=md.convert(post.body)
		post.toc=md.toc
		return post
	def get_context_data(self,**kwargs):
		context=super(PostDetailView,self).get_context_data(**kwargs)
		form=CommentForm()
		comment_list=self.object.comment_set.all()
		context.update({
			'form': form,
			'comment_list': comment_list,
			})
		return context
'''
def search(request):
	q=request.GET.get('q')
	error_msg=''
	if not q:
		error_msg="请输入关键词"
		return render(request,'blog/index.html',{'error_msg':error_msg})
	post_list=Post.objects.filter(Q(title__icontains=q)|Q(body__icontains=q))
	return render(request,'blog/index.html',{'error_msg':error_msg,'post_list':post_list})

def contact(request):

	body='###<center>Me</center>\n<br>1998年于福建晋江出产的雄性\n\n2010年进入养正中学\n\n2016进入厦门理工学院软件工程学院\n\n未完待续...<br><br><br><br>\n###<center>The blog</center>\n<br>由Django搭建，用的服务器和域名都来自于阿里云\n\n模仿追梦人物的博客搭建，十分感谢他的博客[zmrenwu.com](http://zmrenwu.com)让我尽快的能将它上线运行，给了我很大的启发。\n\n目前是非常简陋的版本，简陋到当前这个页面是直接用前端写的（因为我也不清楚如何最简的创建一个单页面），我会加紧学习尽快完善它。<br><br><br><br>\n###<center>Contact</center>\n<br><center>[My Github](https://github.com/DumplingsYang)</center>'
	md=markdown.Markdown(extensions=[
		'markdown.extensions.extra',
		'markdown.extensions.codehilite',
		'markdown.extensions.toc'
		])
	body=md.convert(body)
	return render(request,'blog/contact.html',{'body':body})
'''def about(request):
	return HttpResponse("about test")
	

def index(request):
	post_list=Post.objects.all().order_by('-created_time')
	return render(request,'blog/index.html',context={'post_list':post_list})

def archives(request,year,month):
	post_list=Post.objects.filter(created_time__year=year,
								created_time__month=month
								).order_by('-created_time')
	return render(request,'blog/index.html',context={'post_list':post_list})

def category(request,pk):
	cate=get_object_or_404(Category,pk=pk)
	post_list=Post.objects.filter(category=cate).order_by('-created_time')
	return render(request,'blog/index.html',context={'post_list':post_list})
'''
def detail(request,post_slug):
	post=get_object_or_404(Post,post_slug=post_slug)
	post.increase_views()
	post.body=markdown.markdown(
		post.body,
		extensions=[
			'markdown.extensions.extra',
			'markdown.extensions.codehilite',
			'markdown.extensions.toc',
		])
	form=CommentForm()
	comment_list=post.comment_set.all()
	context={
			'post':post,
			'form':form,
			'comment_list':comment_list
	}
	return render(request,'blog/detail.html',context=context)


