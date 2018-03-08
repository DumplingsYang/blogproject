from django.conf.urls import url 
from .import views

app_name = 'account'
urlpatterns=[
	url(r'account/register/$',views.register,name='register'),
	url(r'account/login/$',views.log_in,name='login'),
	url(r'account/logout/$',views.log_out,name='logout'),
]