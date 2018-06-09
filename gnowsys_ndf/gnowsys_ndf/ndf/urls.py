from django.conf.urls import url
from . import views
app_name = 'ndf'
urlpatterns=[
	url(r'^create/', views.create , name = 'create'),
	url(r'^read/', views.read , name = 'read'),	
   	url(r'^update/', views.update , name ='update'),
	url(r'^delete/', views.delete , name = 'delete')]
