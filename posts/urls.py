from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^post_stuff/$', views.post, name="stuff"),
]