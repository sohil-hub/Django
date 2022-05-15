from django.shortcuts import render, redirect
from django.http import request, HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile, Post



# Create your views here.

@login_required(login_url='signin')
def index(request):
    user_profile = Profile.objects.get(user=request.user)
    posts = Post.objects.all()
    return render(request, 'index.html', {"user_profile": user_profile, "posts": posts})

def signIn(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        messages.info(request, 'Invalid Credentials')
        return redirect('signin')
    return render(request=request, template_name='signin.html')

def signUp(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password_2 = request.POST['password_2']

        if password != password_2:
            messages.info(request=request, message='Passwords should be same')
            return redirect('signup')
        if User.objects.filter(username=username):
            messages.info(request=request, message='username is taken')
            return redirect('signup')
        if User.objects.filter(email=email):
            messages.info(request=request, message='email is taken')
            return redirect('signup')
        
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        #log user in and redirect to settings page
        user_login = auth.authenticate(username=username, password=password)
        auth.login(request, user_login)
        #create a Profile object for the new user
        user_model = User.objects.get(username=username)
        new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
        new_profile.save()

        return redirect('setting')
    
    return render(request=request, template_name='signup.html')

@login_required(login_url='signin')
def logOut(request):
    auth.logout(request)
    return redirect('signin')

@login_required(login_url='signin')
def upload(request):
    if request.method == "POST":
        user = request.user.username
        image = request.FILES.get("image_upload")
        caption = request.POST["caption"]

        new_post = Post(user=user, image=image, caption=caption)
        new_post.save()

    return redirect('index')

@login_required(login_url='signin')
def setting(request):
    user_profile = Profile.objects.get(user=request.user)

    if request.method == "POST":
        image = user_profile.profile_image
        bio = request.POST['bio']
        location = request.POST['location']

        if request.FILES.get("image") != None:
            image = request.FILES.get("image")
        user_profile.profile_image = image
        user_profile.bio = bio
        user_profile.location = location
        user_profile.save()

        return redirect('setting')
    return render(request, 'setting.html', {'user_profile': user_profile})