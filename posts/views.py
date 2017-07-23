from django.shortcuts import render
from .models import Post
from django.shortcuts import get_object_or_404

def post_list(request):
	obj_list = Post.objects.all()
	context = {
		"obj_list": obj_list,
		

	}
	return render(request, 'post_list.html', context)

def post_detail(request, post_id):
	obj = get_object_or_404(Post, id=post_id)
	context = {
		"instance": obj,
		"user": request.user,

	}
	return render(request, 'post_detail.html', context)