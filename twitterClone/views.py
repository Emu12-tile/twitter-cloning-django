from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Profile, Meep
from .forms import MeepForm, SignUpForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
# Create your views here.
def home(request):
    if request.user.is_authenticated:
        form=MeepForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                meep=form.save(commit=False)
                meep.user=request.user
                meep.save()
                messages.success(request, ("You Tweet has been Posted  "))
                return redirect('home')
        meeps=Meep.objects.all().order_by("created_at")
        return render(request,'home.html',{"meeps":meeps,"form":form})
    else:
        meeps=Meep.objects.all().order_by("created_at")
        return render(request,'home.html',{"meeps":meeps})
def profile_list(request):
    if request.user.is_authenticated:
      profiles=Profile.objects.exclude(user=request.user)
      return render(request, 'profile_list.html',{"profiles":profiles})
    else:
        messages.success(request, ("You Must Be Logged In To View This Page "))
        return redirect('home')
def profile(request,pk):
    if request.user.is_authenticated:

        profile=Profile.objects.get(user_id=pk)
        meeps=Meep.objects.filter(user_id=pk)
        if request.method=="POST":
            current_user_profile=request.user.profile
            action=request.POST['follow']
            if action=="unfollow":
                current_user_profile.follows.remove(profile)
            elif action=="follow":current_user_profile.follows.add(profile)
            current_user_profile.save()
        return render(request, "profile.html", {"profile":profile,"meeps":meeps})
    else:
        return redirect('home')
    
def login_user(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("You Have Been Logged In! "))
            return redirect('home')
        else:
             messages.success(request, ("There Was an Error Please Try Again! "))
             return redirect('login')

    else:
        
        return render(request, "login.html", {})

def logout_user(request):
    
    logout(request)
    messages.success(request, ("You Have Been Logged Out! "))
    return redirect('home')

def register_user(request):
     form=SignUpForm()
     if request.method=="POST":
         form=SignUpForm(request.POST)
         if form.is_valid():
             form.save()
             username=form.cleaned_data['username']
             password=form.cleaned_data['password1']
            #  first_name=form.cleaned_data['first_name']
            #  last_name=form.cleaned_data['last_name']
            #  email=form.cleaned_data['email']
             user=authenticate(username=username,password=password)
             login(request,user)
             messages.success(request, ("You Registered Successfully! "))
             return redirect('home')
     return render(request, "register.html", {'form':form})


def update_user(request):
    if request.user.is_authenticated:
        current_user= User.objects.get(id=request.user.id)
        form=SignUpForm(request.POST or None, instance=current_user)
        if form.is_valid():
            form.save()
            login(request,current_user)
            messages.success(request, ("Your Profile Upadated! "))
            return redirect('home')
        return render(request, "update_user.html", {'form':form})
    else:
        messages.success(request, ("You Must Be login! "))
        return redirect('home')

    
