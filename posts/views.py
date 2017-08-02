from django.shortcuts import render, redirect
from .models import Post, Like
from .forms import PostForm, UserSignUp, UserLogin
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from urllib.parse import quote
from django.http import Http404, JsonResponse
from django.utils import timezone

from django.contrib.auth import authenticate, login, logout


def like_button(request, post_id):
	obj = Post.objects.get(id=post_id)

	like, created = Like.objects.get_or_create(user=request.user, post=obj)

	if created:
		action = "Like"
	else:
		like.delete()
		action="unlike"

	post_like_count = obj.like_set.all().count()
	context = {
		"action": action,
		"like_count": post_like_count,
	}

	return JsonResponse(context, safe=False)


def userlogout(request):
	logout(request)
	return redirect("posts:list")


def usersignup(request):
	context = {}
	form = UserSignUp()
	context['form'] = form
	if request.method == "POST":
		form = UserSignUp(request.POST)
		if form.is_valid():
			user = form.save()
			username = user.username
			password = user.password
			user.set_password(password)
			user.save()
			auth_user = authenticate(username=username, password=password)
			login(request, auth_user)


			return redirect("posts:list")
		messages.warning(request, forms.errors)
		return redirect("posts:signup")
	return render(request, 'signup.html', context)


def userlogin(request):
	context = {}
	form = UserLogin()
	context['form'] = form
	if request.method == "POST":
		form = UserLogin(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']

			auth_user = authenticate(username=username, password=password)
			if auth_user is not None: 
				login(request, auth_user)
				return redirect("posts:list")

			messages.warning(request, "Wrong username or password combination")
			return redirect("posts:login")
		messages.warning(request, form.errors)
		return redirect("posts:login")
	return render(request, 'login.html', context)

 
def post_list(request):
	today = timezone.now().date()
	if request.user.is_staff or request.user.is_superuser:
		obj_list =  Post.objects.all()
	else: 
		obj_list = Post.objects.filter(draft=False).filter(publish__lte=today)
	paginator = Paginator(obj_list, 6) # Show 4 contacts per page
	page = request.GET.get('page')
	try:
		objects = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		objects = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		objects = paginator.page(paginator.num_pages)


	context = {
		"post_list": objects,
	

	}
	return render(request, 'post_list.html', context)

def post_detail(request, slug):
	obj = get_object_or_404(Post, slug = slug)
	
	if request.user.is_authenticated():
		if Like.objects.filter(post=obj, user=request.user).exists():
			liked = True
		else:
			liked = False

	post_like_count = obj.like_set.all().count()

	context = {
		"instance": obj,
		"user": request.user,
	    "post_like_count":post_like_count,
    	"liked":liked

	}
	return render(request, 'post_detail.html', context)

def post_create(request):
	if not (request.user.is_staff or request.user.is_superuser):
		raise Http404
	form = PostForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		obj = form.save(commit=False)
		obj.author = request.user
		obj.save()
		messages.success(request, "Congratulations on creating a Post")
		return redirect("posts:list")
	context = {
		"form":form,
	}
	return render(request, 'post_create.html', context)

def post_update(request, slug):
	if not (request.user.is_staff or request.user.is_superuser):
		raise Http404
	post_object = get_object_or_404(Post, slug=slug)
	form = PostForm(request.POST or None,  request.FILES or None, instance=post_object)
	if form.is_valid():
		form.save()
		messages.success(request, "Your Post Has Been Updated")
		return redirect("posts:list")
	context = {
		"form":form,
		"post_object":post_object,
	}
	return render(request, 'post_update.html', context)

def post_delete(request, slug):
	if not (request.user.is_superuser):
		raise Http404
	Post.objects.get(slug=slug).delete()
	messages.warning(request, "Post Has Been Deleted")
	return redirect("posts:list")

