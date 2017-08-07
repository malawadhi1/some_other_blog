from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings 
from django.conf.urls.static import static 


# from posts.views import post_home

urlpatterns = [
	url(r'^admin/', admin.site.urls),
    url(r'^posts/', include('posts.urls', namespace="posts")),
    url(r'^comments/', include('django_comments.urls')),
    url(r'^api/', include('api.urls', namespace="api")),
]

if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
	