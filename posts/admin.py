from django.contrib import admin

from .models import Post, Like

class PostModelAdmin(admin.ModelAdmin):
	list_display = ["title", "timestamp",]
	search_fields = ["title", "content"]
	
	
class Meta:
	model = Post

admin.site.register(Post, PostModelAdmin)
admin.site.register(Like)