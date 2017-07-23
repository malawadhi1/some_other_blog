from django.conf.urls import url
from posts import views

urlpatterns = [
    url(r'^whatever/$', views.post_create, name="whatever"),
]