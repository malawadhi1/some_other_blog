from django.shortcuts import render
from .models import Post
from django.shortcuts import get_object_or_404

def post_create(request):
	obj = get_object_or_404(Post, id=2)
	context = {
		"instance": obj,

	}
	return render(requesr, 'whatever.html', context)