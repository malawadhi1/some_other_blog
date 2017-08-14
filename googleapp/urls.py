from django.conf.urls import url 
from . import views

urlpatterns = [
	url(r'^text', views.text_search, name='text'),
	url(r'^detail', views.place_detail, name='detail'),
	url(r'^radius', views.radius_search, name='radius'),
]