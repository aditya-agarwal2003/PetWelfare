from django.shortcuts import render,redirect
from django.urls import reverse
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required
from pet_adoption.models import Post, AdoptionRequest
# from django.http import HttpResponse



# Create your views here.
def register(request):

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split("@")[0]
            user = Account.objects.create_user(first_name=first_name,last_name=last_name,email=email,username=username,password=password)
            user.phone_number = phone_number
            user.save()
            if user is not None:
                auth.login(request,user)
                messages.success(request,'Registration Successfull')

                return redirect('dashboard')
    else:
        form = RegistrationForm()
    context = {
        'form' : form,
    }
    return render(request,'accounts/register.html',context)


def login(request):

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email = email,password = password)


        if user is not None:
            auth.login(request,user)
            messages.success(request,'You are logged in now')

            return redirect('dashboard')
        else:
            messages.error(request,'Invalid email or password')
            return redirect('login')
    return render(request,'accounts/login.html')


@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    messages.success(request,'You are Logged Out!')
    return redirect('login')


@login_required(login_url = 'login')
def dashboard(request):
    data = {}
    user = request.user
    posts = Post.objects.filter(
        user=user, is_active=True
    ).order_by('-created_at')
    data['posts'] = posts
    data['requests'] = AdoptionRequest.objects.filter(
        user=user, is_active=True
    )
    data['posts_count'] = posts.count()
    return render(request, 'accounts/dashboard.html', data)