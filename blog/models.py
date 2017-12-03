from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.html import strip_tags
from django.utils.text import slugify
import markdown


# Create your models here.
class Category(models.Model):
	name=models.CharField(max_length=100)
	def __str__(self):
		return self.name
	
class Tag(models.Model):
	name=models.CharField(max_length=100)
	def __str__(self):
		return self.name

class Post(models.Model):
	title=models.CharField(max_length=70)
	body=models.TextField()
	created_time=models.DateTimeField()
	modified_time=models.DateTimeField()
	excerpt=models.CharField(max_length=200,blank=True)
	category=models.ForeignKey(Category)
	tags=models.ManyToManyField(Tag,blank=True)
	author=models.ForeignKey(User)
	views=models.PositiveIntegerField(default=0)
	excerpt=models.CharField(max_length=100,blank=True)
	post_slug=models.SlugField(max_length=15,unique=True,blank=True)
	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('blog:detail',kwargs={'post_slug':self.post_slug})

	def increase_views(self):
		self.views+=1
		self.save(update_fields=['views'])

	def get_unique_slug(self):
		slug = slugify(self.title)
		unique_slug = slug
		num = 1
		while Post.objects.filter(post_slug=unique_slug).exists():
			unique_slug = '{}-{}'.format(slug,num)
			num+=1
		return unique_slug

	def save(self,*args,**kwargs):
		if not self.excerpt:
			md=markdown.Markdown(extensions=[
				'markdown.extensions.extra',
				'markdown.extensions.codehilite',
				])
			self.excerpt=strip_tags(md.convert(self.body))[:54]
		if not self.post_slug:
			self.post_slug=self.get_unique_slug()
		super(Post,self).save(*args,**kwargs)
	

