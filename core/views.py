from django.shortcuts import render, redirect,get_object_or_404
from django.http import JsonResponse
from .forms import NewUserForm
from django.contrib.auth import login, authenticate,logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .models import *
from .forms import BlogForm
import requests
from dotenv import load_dotenv
import os


load_dotenv()
API_KEY = os.getenv("API_KEY")


# Create your views here.
def index(request):
	all_blogs = Blog.objects.all()
	response = requests.get(url=f'https://api.openweathermap.org/data/2.5/weather?lat=40&lon=50&appid={API_KEY}')
	data = int(response.json()['main']['temp'])
	api_data = round(data-273.15)
	return render(request,'index.html',{'all_blogs':all_blogs,'api_data':f"{api_data}°C"})


def contact(request):
	return render(request,'contact.html')

def about(request):
	return render(request,'about.html')

def blog_detail(request,pk):
	blog = Blog.objects.get(id=pk)
	comments = blog.comments.all().order_by('-date')
	likes = Like.objects.filter(blog=blog).count()
	session_key = request.session.session_key
	is_like = Like.objects.filter(blog=blog, session_key=session_key).exists()
	return render(request,'post.html',{'blog':blog,'comments':comments,'likes':likes,'is_like':is_like})

def like_blog(request, blog_id):
	blog = get_object_or_404(Blog,id=blog_id)
	session_key = request.session.session_key
	if not Like.objects.filter(blog=blog, session_key=session_key).exists():
		Like.objects.create(blog=blog, session_key=session_key)
		return JsonResponse({'message': 'Blog liked successfully!','info':'like'})
	else:
		Like.objects.filter(blog=blog, session_key=session_key).delete()
	return JsonResponse({'message': 'Blog unliked successfully!',})

def write_comment(request,pk):
	if request.method == "POST":
		content = request.POST.get('content')
		if request.user.is_authenticated == False:
			messages.warning(request, "You are not authorized")
			return JsonResponse({'msg':'Failure'})
		if content == '':
			messages.info(request, "You should add something")
			return JsonResponse({'msg':'Failure'})
		
		blog = Blog.objects.get(id=pk)
		new_comment = Comment.objects.create(blog=blog,author=request.user,content=content)
		new_comment.save()
		messages.success(request, "Added comment successfully")
		return JsonResponse({'msg':'Success'})

def new_blog(request):
	form = BlogForm()
	if request.method == "POST":
		form = BlogForm(request.POST)
		if form.is_valid():
			blog = form.save(commit=False)
			if request.user.is_authenticated:
				blog.author = request.user
			else:
				blog.author = 'Anonymous User'
			blog.save()  
		return redirect('index') 				
	return render(request,'blog_create.html',{'form':form})

def register_view(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request,user)
			return redirect("login")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request=request, template_name="register.html", context={"register_form":form})

def login_view(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				return redirect("index")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="login.html", context={"login_form":form})

def logout_view(request):
	logout(request)
	return redirect("index")