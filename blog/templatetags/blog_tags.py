from ..models import Post,Category,Tag
from django import template
from django.db.models.aggregates import Count
import markdown
register=template.Library()

@register.simple_tag
def get_recent_posts(num=5):
	return Post.objects.all().order_by('-created_time')[:num]

@register.simple_tag
def archives():
	return Post.objects.dates('created_time','month',order='DESC')

@register.simple_tag
def get_categories():
	return Category.objects.all()

@register.simple_tag
def get_tag():
	return Tag.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)

@register.filter(name='mdfilter')
def mdfilter(value):
	value=markdown.markdown(
		value,
		extensions=[
		'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
		])
	return value