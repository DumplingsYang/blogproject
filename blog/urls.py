#blog/urls.py
from django.conf.urls import url 
from . import views

app_name='blog'
urlpatterns=[
	url(r'^$',views.IndexView.as_view(),name='index'),
	url(r'^post/(?P<post_slug>[-\w\d]+)/$',views.detail,name='detail'),
	url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$',views.ArchivesViews.as_view(),name='archives'),
	url(r'^category/(?P<pk>[0-9]+)/$',views.CategoryViews.as_view(),name='category'),
	url(r'^tag/(?P<pk>[0-9]+)/$',views.TagView.as_view(),name='tag'),
	url(r'^search/$',views.search,name='search'),
]